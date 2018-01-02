var noble = require('noble');

noble.on('stateChange', function(state)
{
	if(state == 'poweredOn')
	{
		console.log('starting scan\n\n');
		noble.startScanning();
	}
	else
	{
		console.log('stopping scan\n\n');
		noble.stopScanning();
	}
});

noble.on('discover', function(peripheral)
{
	console.log('Found device with local name: ' + peripheral.advertisement.localName);
	console.log('advertising the following service uuid\'s: ' + peripheral.advertisement.serviceUuids);
	console.log('peripheral uuid: ' + peripheral.uuid);
	console.log();
});
