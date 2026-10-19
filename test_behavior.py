import unittest
from fits_hdu_map import inspect,example,value

def change(b,index,key,val,base=0):
 b=bytearray(b);b[base+index*80:base+(index+1)*80]=(key.ljust(8)+'= '+(val if val.startswith("'") else val.rjust(20))).ljust(80).encode();return bytes(b)
class Behavior(unittest.TestCase):
 def test_primary_and_extension(self):
  r=inspect(example());self.assertEqual([x['data_range'] for x in r['hdus']],[[2880,2880],[5760,5764]]);self.assertEqual(r['findings'],[])
 def test_float_extent(self):
  b=change(example(),1,'BITPIX','-64',2880);r=inspect(b);self.assertEqual(r['hdus'][1]['data_range'],[5760,5792])
 def test_zero_axis(self):
  b=change(example()[:5760],3,'NAXIS1','0',2880);self.assertEqual(inspect(b)['hdus'][1]['data_range'],[5760,5760])
 def test_padding_finding(self):
  b=bytearray(example());b[-1]=1;self.assertEqual(inspect(b)['findings'][0]['kind'],'nonzero_data_padding')
 def test_header_padding(self):
  b=bytearray(example());b[500]=0
  with self.assertRaises(ValueError):inspect(b)
 def test_order_and_duplicate(self):
  for b in (change(example(),2,'NAXIS1','0'),change(example(),3,'BITPIX','8')):
   with self.assertRaises(ValueError):inspect(b)
 def test_extension_contract(self):
  for b in (change(example(),3,'EXTEND','F'),change(example(),0,'XTENSION',"'BINTABLE'",2880),change(example(),5,'PCOUNT','1',2880)):
   with self.assertRaises(ValueError):inspect(b)
 def test_missing_end_and_truncation(self):
  for b in (example()[:-1],example()[:2880].replace(b'END'+b' '*77,b' '*80)):
   with self.assertRaises(ValueError):inspect(b)
 def test_axis_boundary(self):
  with self.assertRaises(ValueError):inspect(change(example(),3,'NAXIS1','1000001',2880))
 def test_quoted_slash(self):self.assertEqual(value("KEY     = 'a/b''c' / comment"),"a/b'c")

 def test_required_fixed_columns(self):
  raw=example();self.assertEqual(raw[10:30],b'                   T');self.assertEqual(raw[90:110],b'                   8')
  for index,key,v in ((0,'SIMPLE','T'),(1,'BITPIX','8')):
   b=bytearray(raw);b[index*80:(index+1)*80]=(key.ljust(8)+'= '+v).ljust(80).encode()
   with self.assertRaisesRegex(ValueError,'column 30'):inspect(b)
