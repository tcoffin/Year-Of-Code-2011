#!/usr/bin/python

import re

spaces = { 0: u'\u0020', 1: u'\u00A0', 2: u'\u2000', 3: u'\u2001', 4: u'\u2002', 5: u'\u2003', 6: u'\u2004', 7: u'\u2005', 8: u'\u2006', 9: u'\u2007', 10: u'\u2008', 11: u'\u2009', 12: u'\u200A', 13: u'\u202F', 14: u'\u205F', 15: u'\u3000' }
rev_spaces = { u'\u0020':0, u'\u00A0':1, u'\u2000':2, u'\u2001':3, u'\u2002':4, u'\u2003':5, u'\u2004':6, u'\u2005':7, u'\u2006':8, u'\u2007':9, u'\u2008':10, u'\u2009':11, u'\u200A':12, u'\u202F':13, u'\u205F':14, u'\u3000':15 }

obfuscation_text = "Screw all of you! I'll make my own steganography! With BlackJack... and hookers! Actually forget the steganography."

p = "this is a hidden message"

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

def decodePayload( enc_payload ):
	payload = ''
	high_bits = 0
	low_bits = 0

	for c in range( 0, len( enc_payload ) - 1 ):

		if c % 2 == 0:
			high_bits = rev_spaces[ enc_payload[c] ] << 4
		else:
			low_bits = rev_spaces [ enc_payload[c] ]
			payload += chr( high_bits | low_bits )
			

	return payload

def hideMessage ( body, payload ):
	enc_payload = encodePayload( payload )
	payload_size = len( enc_payload )
	morebody = body
	output = ''
	c = 0

	# determine if the body is big enough, if not repeat it.
	if morebody.count( " " ) < payload_size:
		for i in range( payload_size / morebody.count( ' ' ) ):
			morebody += ' ' + body

	words = morebody.split( ' ' )	

	for i in range( 0, len( words ) - 1 ):
		output += words[ i ]
		if i < len( enc_payload ):
			output += enc_payload[ i ]
		else:
			output += ' '

	return output

def showMessage( body ):
	pattern = '['
	for x,y in spaces.iteritems():
		pattern += y

	pattern += ']'

	pieces = re.findall( pattern, body, re.U )
	
	return decodePayload ( pieces )

foo = hideMessage( obfuscation_text, p )
print foo
print showMessage( foo )
