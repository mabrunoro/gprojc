var Bleacon = require('bleacon')

// var uuid = 'b9407f30-f5f8-466e-aff9-25556b57fe6d';
// var uuid = 'b9407f30f5f8466eaff925556b57fe6d';
// var major = 37438; // 0 - 65535
// var minor = 4733; // 0 - 65535

// Bleacon.startScanning([uuid], [major], [minor]);
Bleacon.startScanning(/*uuid*/);

Bleacon.on('discover',function(bleacon) {
	console.log('uuid: ' + bleacon.uuid);
	console.log('major: ' + bleacon.major);
	console.log('minor: ' + bleacon.minor);
	console.log('measuredPower: ' + bleacon.measuredPower);
	console.log('accuracy: ' + bleacon.accuracy);
	console.log('proximity: ' + bleacon.proximity);
	console.log();
});
