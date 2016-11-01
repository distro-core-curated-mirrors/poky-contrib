from oeqa.selftest.base import oeSelfTest
from oeqa.utils.decorators import testcase
from oe.maketype import create, factory

class TestTypes(oeSelfTest):
    def assertIsInstance(self, obj, cls):
        return self.assertTrue(isinstance(obj, cls))

    def assertIsNot(self, obj, other):
        return self.assertFalse(obj is other)

    def assertFactoryCreated(self, value, type, **flags):
        cls = factory(type)
        self.assertIsNot(cls, None)
        self.assertIsInstance(create(value, type, **flags), cls)

    def assertListIsEqual(self, value, valid, sep=None):
        obj = create(value, 'list', separator=sep)
        self.assertListEqual(obj, valid)

class TestBooleanType(TestTypes):
    def test_invalid(self):
        self.assertRaises(ValueError, create, '', 'boolean')
        self.assertRaises(ValueError, create, 'foo', 'boolean')
        self.assertRaises(TypeError, create, object(), 'boolean')

    def test_true(self):
        self.assertTrue(create('y', 'boolean'))
        self.assertTrue(create('yes', 'boolean'))
        self.assertTrue(create('1', 'boolean'))
        self.assertTrue(create('t', 'boolean'))
        self.assertTrue(create('true', 'boolean'))
        self.assertTrue(create('TRUE', 'boolean'))
        self.assertTrue(create('truE', 'boolean'))

    def test_false(self):
        self.assertFalse(create('n', 'boolean'))
        self.assertFalse(create('no', 'boolean'))
        self.assertFalse(create('0', 'boolean'))
        self.assertFalse(create('f', 'boolean'))
        self.assertFalse(create('false', 'boolean'))
        self.assertFalse(create('FALSE', 'boolean'))
        self.assertFalse(create('faLse', 'boolean'))

    def test_bool_equality(self):
        self.assertEqual(create('n', 'boolean'), False)
        self.assertNotEqual(create('n', 'boolean'), True)
        self.assertEqual(create('y', 'boolean'), True)
        self.assertNotEqual(create('y', 'boolean'), False)

class TestList(TestTypes):

    def test_list_nosep(self):
        testlist = ['alpha', 'beta', 'theta']
        self.assertListIsEqual('alpha beta theta', testlist)
        self.assertListIsEqual('alpha  beta\ttheta', testlist)
        self.assertListIsEqual('alpha', ['alpha'])

    def test_list_usersep(self):
        self.assertListIsEqual('foo:bar', ['foo', 'bar'], ':')
        self.assertListIsEqual('foo:bar:baz', ['foo', 'bar', 'baz'], ':')
