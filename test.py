
# Generating letterlist of ord() for all english and german letters

letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","Ü","ü","ö","Ö","ä","Ä","ß"]

letterlist = []

for letter in letters:
	#print (ord(letter))
	letterlist.append(ord(letter))

print (letterlist)