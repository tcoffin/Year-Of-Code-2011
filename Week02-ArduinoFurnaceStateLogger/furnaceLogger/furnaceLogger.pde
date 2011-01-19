/* This is a little program that reads the state of my furnace. It's really not all that interesting right now but it's my first arduino program, so the learning process is pretty fun.

I'm a software guy so I'm still kind of fuzzy on how to wire the circuit properly. I know the furnace wire is 25v but not (yet) sure how to work with that voltage.
I prototyped the below software using a button attached to digital pin 2. When pin 2 is high, the furnace is active. 

It stores the state of the furnace in a file called furnace.log.
*/
#include <SdFat.h>
#include <SdFatUtil.h>
#include <ctype.h>

Sd2Card card;
SdVolume volume;
SdFile root;
SdFile file;

char filename[] = "furnace.log";
char writebuffer[256];
char in_byte=0;
char pos=0;
int furnace_state=-1;
int furnacePin = 2;
int ledPin = 7;

void setup(void)
{
	Serial.begin( 9600 );
	pinMode( 10, OUTPUT ); 		// output PIN for the SD slot
	card.init();			// set up the card for i/o
	volume.init( card );		// set up for the volume
	root.openRoot( volume );	// open the root directory of the volume

	pinMode( furnacePin, INPUT );	// the furnance wire input pin (this needs to be pulled down from 24v to 5v)
	pinMode( ledPin, OUTPUT );	// led for when furnace LED is live
}

void loop( void )
{
	file.open( root, filename, O_CREAT | O_APPEND | O_WRITE );	// open the file ( create the file or open it ) for write

	// read in the furnace state
	furnace_state = digitalRead( furnacePin );
	if ( furnace_state == HIGH )
	{
		// write state in to the buffer
		sprintf( writebuffer, "1\n" );
		digitalWrite( ledPin, LOW );
	}
	else
	{
		// write state in to the buffer
		sprintf( writebuffer, "0\n" );
		digitalWrite( ledPin, HIGH );
	}

	file.print ( writebuffer ); 					// write out the data
	file.close();
        delay(1000);
}
