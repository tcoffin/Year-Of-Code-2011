#!/usr/bin/python

spaces = { 0: u'\u0020', 1: u'\u00A0', 2: u'\u2000', 3: u'\u2001', 4: u'\u2002', 5: u'\u2003', 6: u'\u2004', 7: u'\u2005', 8: u'\u2006', 9: u'\u2007', 10: u'\u2008', 11: u'\u2009', 12: u'\u200A', 13: u'\u202F', 14: u'\u205F', 15: u'\u3000' }

obfuscation_text = "Screw all of you! I'll do my own steganobot! With blackjack... And hookers. Actually forget the steganobot."

p = "I want to grape you in the mouth!"


# each character will be encoded as two whitespace characters
def encodePayload( payload ):
	enc_payload = []

	for c in payload:
		# seperate the high 4 bits from the low 4 bits 
		high_bits = ord( c ) >> 4

		low_bits = ord( c ) - ( high_bits << 4 )

		enc_payload.append( spaces[ high_bits ] )
		enc_payload.append( spaces[ low_bits ] )

	return enc_payload

def hideMessage ( body, payload ):
	enc_payload = encodePayload( payload )
	payload_size = len( enc_payload )
	morebody = body
	output = ''
	c = 0

	# determine if the body is big enough, if not repeat it.
	if body.count( " " ) < payload_size:
		for i in range( payload_size / body.count( ' ' ) ):
			morebody += ' ' + body

	words = morebody.split( ' ' )	

	for i in enc_payload:
		output += words[ c ]
		output += i
		c += 1

	return output

print hideMessage( obfuscation_text, p )
