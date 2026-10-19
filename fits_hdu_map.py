"""Map physical bytes in a strict FITS primary/IMAGE HDU subset."""
import argparse
import hashlib
import json
import math
import re
import sys


def value(card):
    if card[8:10]!='= ': raise ValueError('structural card requires = marker')
    s=card[10:].lstrip()
    if s.startswith("'"):
        result='';i=1
        while i<len(s):
            if s[i]=="'":
                if i+1<len(s) and s[i+1]=="'":result+="'";i+=2;continue
                if s[i+1:].strip() and not s[i+1:].lstrip().startswith('/'):
                    raise ValueError('text after quoted value')
                return result.rstrip()
            result+=s[i];i+=1
        raise ValueError('unterminated string')
    return s.split('/',1)[0].strip()


def inspect(raw):
    if not raw or len(raw)>8388608 or len(raw)%2880: raise ValueError('file must be 1..8 MiB in complete FITS blocks')
    offset=0;hdus=[];findings=[];extend=False
    while offset<len(raw):
        if len(hdus)>=32:raise ValueError('at most 32 HDUs')
        cards=[];values={};end=None
        for i in range(144):
            pos=offset+i*80
            if pos+80>len(raw):raise ValueError('truncated header')
            try:c=raw[pos:pos+80].decode('ascii')
            except UnicodeError:raise ValueError('non-ASCII header') from None
            if any(ord(x)<32 or ord(x)>126 for x in c):raise ValueError('nonprinting header character')
            key=c[:8].strip()
            if key=='END':
                if c[8:].strip():raise ValueError('invalid END card')
                end=pos+80;break
            if not re.fullmatch(r'[A-Z0-9_-]{0,8}',key):raise ValueError('unsupported keyword')
            cards.append(key)
            if key in {'SIMPLE','XTENSION','BITPIX','NAXIS','PCOUNT','GCOUNT','EXTEND','GROUPS'} or re.fullmatch(r'NAXIS\d+',key):
                if key in values:raise ValueError('duplicate structural keyword')
                if (key=='XTENSION') != c[10:].lstrip().startswith("'"):
                    raise ValueError('incorrect structural value type')
                values[key]=value(c)
        if end is None:raise ValueError('END absent within four header blocks')
        data_start=((end+2879)//2880)*2880
        if data_start>len(raw) or any(b!=32 for b in raw[end:data_start]):raise ValueError('header padding must be spaces')
        primary=not hdus
        if cards[:3]!=['SIMPLE' if primary else 'XTENSION','BITPIX','NAXIS']:
            raise ValueError('incorrect structural card order')
        if primary and values.get('SIMPLE')!='T':raise ValueError('primary SIMPLE must be T')
        if not primary and values.get('XTENSION')!='IMAGE':raise ValueError('only IMAGE extensions supported')
        def integer(key):
            s=values.get(key,'')
            if not re.fullmatch(r'[+-]?\d+',s):raise ValueError('invalid integer '+key)
            return int(s)
        bitpix=integer('BITPIX');n=integer('NAXIS')
        if bitpix not in (8,16,32,64,-32,-64) or not 0<=n<=4:raise ValueError('unsupported BITPIX/NAXIS')
        names=['NAXIS'+str(i+1) for i in range(n)]
        if cards[3:3+n]!=names or any(k.startswith('NAXIS') and k!='NAXIS' and k not in names for k in values):
            raise ValueError('axis cards must be consecutive and match NAXIS')
        axes=[integer(k) for k in names]
        if any(not 0<=x<=1000000 for x in axes):raise ValueError('axis size limit')
        if values.get('GROUPS','F')!='F':raise ValueError('random groups unsupported')
        if primary:
            extend=values.get('EXTEND')=='T'
            if 'EXTEND' in values and values['EXTEND'] not in ('T','F'):raise ValueError('invalid EXTEND')
            if 'PCOUNT' in values or 'GCOUNT' in values:raise ValueError('primary group parameters unsupported')
        elif not extend or cards[3+n:5+n]!=['PCOUNT','GCOUNT'] or integer('PCOUNT')!=0 or integer('GCOUNT')!=1:
            raise ValueError('IMAGE needs EXTEND=T, PCOUNT=0, GCOUNT=1 in order')
        size=abs(bitpix)//8*math.prod(axes) if n else 0
        end_data=data_start+size;next_offset=((end_data+2879)//2880)*2880
        if next_offset>len(raw):raise ValueError('declared data extends beyond file')
        if any(raw[end_data:next_offset]):findings.append({'hdu':len(hdus),'kind':'nonzero_data_padding'})
        hdus.append({'index':len(hdus),'kind':'PRIMARY' if primary else 'IMAGE','axes':axes,'bitpix':bitpix,
                     'header_range':[offset,data_start],'data_range':[data_start,end_data],
                     'padding_range':[end_data,next_offset],'card_count':len(cards)+1})
        offset=next_offset
    return {'sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),'hdus':hdus,'findings':findings,
            'checksums':'CHECKSUM/DATASUM not verified'}


def example():
    def card(k,v):return (k.ljust(8)+'= '+v).ljust(80).encode('ascii')
    def header(cards):
        b=b''.join(card(k,v) for k,v in cards)+b'END'.ljust(80)
        return b.ljust((len(b)+2879)//2880*2880,b' ')
    return (header([('SIMPLE','T'),('BITPIX','8'),('NAXIS','0'),('EXTEND','T')])+
            header([('XTENSION',"'IMAGE   '"),('BITPIX','8'),('NAXIS','2'),('NAXIS1','2'),('NAXIS2','2'),('PCOUNT','0'),('GCOUNT','1')])+bytes(range(4))+bytes(2876))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',nargs='?');p.add_argument('--make-example');a=p.parse_args()
    try:
        if bool(a.input)==bool(a.make_example):raise ValueError('specify input OR --make-example NEW_FILE')
        if a.make_example:
            with open(a.make_example,'xb') as f:f.write(example())
            return 0
        with open(a.input,'rb') as f:raw=f.read(8388609)
        r=inspect(raw);print(json.dumps(r,indent=2));return int(bool(r['findings']))
    except (OSError,ValueError,UnicodeError) as e:print(str(e),file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())
