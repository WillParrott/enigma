
# The turnover on rotor is determined by that to its right. So the right hand rotor rotates with every key stroke
# We take 3 rortos and a fixed reflector 10 pairs of letters are exchanged in the plugboard
# Settings rotors left to right, starting letters left to right letter pairs
# The problem is that when a rotor rotates, the input and output move. Take I for example. An A coming in from the right is mapped to an E. Now if we shift the rotor 1 place, the A coming in goes into to B, which is mapped to a K. However, this K has also moved around one, so it is read as a J.
# To repicate this, stpeeing a rota moves self.order, in this case so that an A would be mapped to a K. But then substitutes the ith letter for the i-1th letter, so that the letter reported by the rotor is what would be measured relative to a fixed ring (i.e the input ring or the reflector).

# Double stepping. This means that when a prawl engages the ratchet of its rotor through the notch in the rotor to the right, it also pushes the rotor to the right on the stroke. This does no affect the right hand rotor as it steps every time anyway, but affects the middle rotor here



alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_.'

class Rotor:        
    def __init__(self,turnover,ordering):
        self.to = turnover
        self.order = ordering
        self.position = 'A'
        
    def setup(self,position):
        self.position = position
        for i in range(alph.index(self.position)):
            new_order = '{0}{1}'.format(self.order.split(self.order[0])[1],self.order[0])
            self.order = new_order
            new_new_order =''
            for element in self.order:
                new_new_order = '{0}{1}'.format(new_new_order,alph[alph.find(element)-1])
            self.order = new_new_order
        
    def step(self):
        new_order = '{0}{1}'.format(self.order.split(self.order[0])[1],self.order[0])
        self.order = new_order
        if alph.index(self.position)+1 < len(alph):
            self.position = alph[alph.index(self.position)+1]
        else:
            self.position = alph[0]
        new_new_order =''
        for element in self.order:
            new_new_order = '{0}{1}'.format(new_new_order,alph[alph.find(element)-1])
        self.order = new_new_order
        
    def fo_action(self,letter):
        pos = alph.find(letter)
        if pos == -1:
            print(letter,'is not an upper case letter')
            return()
        else:
            return(self.order[pos])
        
    def re_action(self,letter):
        pos = self.order.find(letter)
        if pos == -1:
            print(letter,'is not an upper case letter')
            return()
        else:
            return(alph[pos])

class Reflector:
    def __init__(self,ordering):
        self.order = ordering
    def action(self,letter):
        pos = alph.find(letter)
        if pos == -1:
            print(letter,'is not an upper case letter')
            return()
        else:
            return(self.order[pos])

def make_rotors(rotors,start_pos):
    I =        Rotor(['R'],'EKMFLGDQV.ZNTOWYHXUSPA_IBRCJ')
    II =       Rotor(['F'],'AJDK_SIRUXBLHWTMCQGZ.NPYFVOE')
    III =      Rotor(['W'],'BDFHJLCPRTXV.ZNYEIWGAKMUSQO_')
    IV =       Rotor(['K'],'ESOVPZJ.AYQUIRHXLNFTGK_DCMWB')
    V =        Rotor(['A'],'VZBRGIT_YUPSDNHLX.AWMJQOFECK')
    VI =   Rotor(['A','N'],'.JPGVOUM_FYQBENHZRDKASXLICTW')
    VII =  Rotor(['A','N'],'NZJHGRC_XMYSWBOUFAIV.LPEKQDT')
    VIII = Rotor(['A','N'],'FK_Q.HTLXOCBJSPDZRAMEWNIUYGV')
    reflector =  Reflector('EJMZALYXVBWFCRQUONTSPIKHGD._')
    left = locals()[rotors[0]]
    mid = locals()[rotors[1]]
    right = locals()[rotors[2]]
    left.setup(start_pos[0])
    mid.setup(start_pos[1])
    right.setup(start_pos[2])
    #print(len(left.order),len(mid.order),len(right.order),len(reflector.order))
    return(reflector,left,mid,right)

def get_setup():
    r = input("Please list the 3 rotor set up from left to right. Choices are I II III IV V VI VII VIII. For example, enter II I IV to chose II as the left hand rotor: ")
    rotors = r.split()
    while len(rotors) != 3 or len(set(rotors)) != len(rotors) :
        r = input("Failed. Please list your 3 different rotors with spaces between: ")
        rotors = r.split()
        
    s = input("Please list the 3 rotor start positions up from left to right. For example, D K Y: ")
    start_pos = s.split()
    while len(start_pos) != 3:
        s = input("Failed. Please list your 3 rotor start positions with spaces between: ")
        start_pos = s.split()
    p = input("Please swap up to 10 distinct pairs of letters in your plug board. For example A-D B-H K-Z will pair these three combinations: ")
    pairs = p.split()
    letters = []
    for element in pairs:
        letters.extend(element.split('-'))
    while len(pairs) > 10 or len(letters) != len(set(letters)):
        letters = []
        p = input("Failed. Please list a maximum of 10 distinct pairings with spaces between: ")
        pairs = p.split()
        for element in pairs:
            letters.extend(element.split('-')) 
    pairs = []
    return(rotors,start_pos,pairs)


def main(): #press key, which rotates rotor, then signal is sent, through plugbord, then through rotors right to left, then through releftor, then back through rotors left to right and plugboard, before producing output
    rotors,start_pos,pairs = get_setup()
    message = ''
    while message != 'OVER':
        reflector,left,mid,right =  make_rotors(rotors,start_pos)
        message = input('Enter your message all in caps. Full stop are permitted, and spaces as _. Type OVER to close: ') 
        output = ''
        for letter in message:
            if mid.position in mid.to:
                left.step()
                mid.step()
            if right.position in right.to:
                mid.step()
            right.step()
            letter = plugboard(letter,pairs)
            letter = (right.fo_action(letter))
            letter = (mid.fo_action(letter))
            letter = (left.fo_action(letter))
            letter = (reflector.action(letter))
            letter = (left.re_action(letter))
            letter = (mid.re_action(letter))
            letter = (right.re_action(letter))
            letter = plugboard(letter,pairs)
            output = '{0}{1}'.format(output,letter)
        print(output)
    return()

def plugboard(letter,pairs):
    for pair in pairs:
        if letter == pair.split('-')[0]:
            letter = pair.split('-')[1]
        elif letter == pair.split('-')[1]:
            letter = pair.split('-')[0]
    return(letter)

main()
