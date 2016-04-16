import unittest
from app.main import Hauser as sut

class DeviceMock():
    def doStuff(self):
        return "Doing Stuff"
    def doExceptionalStuff(self, exceptionType):
        raise exceptionType

    def doStuffWithArgs(self, **kwargs):
        return kwargs

class SanityTests(unittest.TestCase):
    def setUp(self):
        self.haus= sut()
        self.devName='devMock'

    def test_canIEvenDoAnObject(self):
        self.assertNotEqual(self.haus, None)

    def test_sanitySelfCheck(self):
        self.assertIn('inspect',self.haus.inspect()[1])

class DevicesManagementTests(unittest.TestCase):
    def setUp(self):
        self.haus= sut()
        self.devName='devMock'
        self.haus.addDevice(DeviceMock, self.devName)

    def assertResultIsError(self, resultToCheck):
        self.assertIn('error',resultToCheck[0])

    def isDeviceOnList(self, deviceName):
        return (deviceName in self.haus.getAllDevices()[1])

    def test_addStaticDevice(self):
        self.assertTrue(self.isDeviceOnList(self.devName))

    def test_addDeviceFromDynamicSource(self):
        self.haus.addDevice('dynamicClass',self.devName, 'dynamic')
        self.assertTrue(self.isDeviceOnList(self.devName))

    def test_addTwoDevsWithSameName(self):
        result= self.haus.addDevice(DeviceMock, self.devName)
        self.assertResultIsError(result)

    def test_removeDevice(self):
        self.haus.removeDevice(self.devName)
        self.assertFalse(self.isDeviceOnList(self.devName))

    def test_removeDeviceSelfReturnResultErrorAndDeviceIsNotRemoved(self):
        result= self.haus.removeDevice('self')
        self.assertResultIsError(result)
        self.assertTrue(self.isDeviceOnList('self'))

    def test_addDeviceWithInterfaceAndRemoveIt(self):
        self.haus.action('self', 'addDevice', deviceClassName= DeviceMock, internalName= self.devName)
        self.assertIn(self.devName , self.haus.getAllDevices()[1])
        self.haus.action('self', 'removeDevice', internalName= self.devName)
        self.assertNotIn(self.devName , self.haus.getAllDevices()[1])

    def test_addDeviceWithInterfaceAndRemoveItWithoutNamedParameters(self):
        self.haus.action('self', 'addDevice', DeviceMock, self.devName)
        self.assertIn(self.devName , self.haus.getAllDevices()[1])
        self.haus.action('self', 'removeDevice', self.devName)
        self.assertNotIn(self.devName , self.haus.getAllDevices()[1])

class PerformActionTests(unittest.TestCase):
    def setUp(self):
        self.haus= sut()
        self.devName='devMock'
        self.haus.addDevice(DeviceMock, self.devName)

    def assertResultIsError(self, resultToCheck):
        self.assertIn('error',resultToCheck['result'])

    def test_inspectOnDevice(self):
        self.assertIn('doStuff',self.haus.inspect(self.devName)[1])

    def test_inspectAllDevices(self):
        otherDevName="device2"
        self.haus.addDevice(DeviceMock, otherDevName)
        result, inspection= self.haus.inspectAll()
        self.assertIn(self.devName, inspection)
        self.assertIn(otherDevName, inspection)

    def test_performActionOnSelfByInterface(self):
        self.assertIn('self', self.haus.action('self', 'getAllDevices')['details'])

    def test_performActionOnDevice(self):
        commandResult= self.haus.action(self.devName,'doStuff')
        self.assertEqual(commandResult['result'], 'ok')

    def test_performActionWithArgumentsOnDevice(self):
        result= self.haus.action(self.devName, 'doStuffWithArgs', arg1=0, arg2='dwa')
        self.assertEquals({'arg1':0, 'arg2':'dwa'}, result['details'])

    def test_performedActionThrowsExceptionExpectDetails(self):
        exceptionInfo='Mock SysError'
        result= self.haus.action(self.devName, 'doExceptionalStuff',SystemError(exceptionInfo))
        self.assertResultIsError(result)
        self.assertIn(exceptionInfo, result['details'])
