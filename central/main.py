class Hauser:
    def __init__(self):
        self._devices={
                'self'   : self}

    def __setitem__(self, internalName, deviceClassNameAndfromWhatModuleTuple):
        deviceClassName, fromWhatModule= deviceClassNameAndfromWhatModuleTuple
        if internalName in self: raise KeyError('error', 'Key "%s" already in use' % internalName)
        if fromWhatModule: self._devices[internalName]= getattr(__import__(fromWhatModule), deviceClassName)
        else: self._devices[internalName]= deviceClassName()

    def __getitem__(self, device):
        if device not in self: raise KeyError('Device %s not installed' % device)
        return ('ok', [cmd for cmd in dir(self._devices[device]) if not cmd.startswith('_')])

    def __iter__(self):
        return self._devices.__iter__()

    def __delitem__(self, device):
        if device not in self._devices: raise KeyError('Device %s don\'t exist and cannot be removed' % device)
        if device == 'self': raise KeyError('Cannot remove "self" device')
        self._devices.pop(device,None)

    def __len__(self):
        return len(self._devices)

    def __contains__(self, deviceName):
        return deviceName in self._devices.keys()

    def action(self, _device, _action, *args, **kwargs):
        try:
            if _device == 'self': result, details= getattr(self._devices[_device], _action)(*args, **kwargs)
            else:
                result= 'ok'
                details= getattr(self._devices[_device], _action)(*args, **kwargs)
        except Exception as e:
            result= 'error'
            details= str(e)
        return { 'result': result, 'details': details}

    def addDevice(self, deviceClassName, internalName, fromWhatModule=None):
        self[internalName]= (deviceClassName, fromWhatModule)
        return self.getAllDevices()

    def removeDevice(self, device):
        self.__delitem__(device)
        return self.getAllDevices()

    def getAllDevices(self):
        return ('ok', [dev for dev in self])

