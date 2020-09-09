from flask import Flask , render_template , flash , redirect , request
import requests
import bs4 as bs

app = Flask(__name__)

title = 'speed'

SPEED = {
        'SPEED X':0.35,
        'SPEED IX':0.34,
        'SPEED VIII':0.31,
        'SPEED VII':0.28,
        'SPEED VI':0.24,
        'SPEED V':0.20,
        'SPEED IV':0.16,
        'SPEED III':0.12,
        'SPEED II':0.08,
        'SPEED I':0.04,
        'TEAM SPEED X':0.12,
        'TEAM SPEED IX':0.11,
        'TEAM SPEED VIII':0.10,
        'TEAM SPEED VII':0.09,
        'TEAM SPEED VI':0.08,
        'TEAM SPEED V':0.07,
        'TEAM SPEED IV':0.06,
        'TEAM SPEED III':0.05,
        'TEAM SPEED II':0.04,
        'TEAM SPEED I':0.03,
    }

TEAM_SPEED = {
        'TEAM SPEED X':0.12,
        'TEAM SPEED IX':0.11,
        'TEAM SPEED VIII':0.10,
        'TEAM SPEED VII':0.09,
        'TEAM SPEED VI':0.08,
        'TEAM SPEED V':0.07,
        'TEAM SPEED IV':0.06,
        'TEAM SPEED III':0.05,
        'TEAM SPEED II':0.04,
        'TEAM SPEED I':0.03,
    }

RANKS = {
        'Rank 0':0,
        'Rank 1':1,
        'Rank 2':2,
        'Rank 3':3,
        'Rank 4':4,
        'Rank 5':5
    }

RUNE_GUARDIAN = {
        '0%':0,
        '2%':0.02,
        '5%':0.05,
        '7%':0.07,
        '10%':0.1
    }

# a function that allow using spaces in monster names
def fix(string):
    new_s = str(string).replace(' ' , '_')

    return new_s

# Main app class **speed**
class Speed():

    # init function
    def __init__(self ):

        # a variable that holds buff value
        self.percent = []

        # a list that holds monster speed at all ranks
        self.spd = []

        self.assign()

    def assign(self):
        for i in range(0 , 11) :
            self.percent.append(0)

    def get_speed(self , urls):

        # resets perent to 0 each time a new monster is searched for
        for i in range(len(self.percent)):
            self.percent[i] = 0
    
        # a variable that hold monster name
        Monster_name = fix(urls)

        # the wiki monster url variable
        url = f'https://monsterlegends.fandom.com/wiki/{Monster_name}#☆'


        page = requests.get(url)

        soup = bs.BeautifulSoup(page.content , 'html.parser')

        speed = []

        # loop through all tables in the wiki 
        for row in soup.find_all('table' , class_='article-table roundy'):

            # find all rows in the table
            row.find_all('tr')

            # loops through all columns in the table
            for col in row.find_all('th'):

                # checks if column text ==  speed
                if col.get_text() == 'Speed':
                    
                    # find the speed value (should be next to 'Speed' text)
                    nextNode = col.nextSibling

                    # break the loop if None
                    if nextNode is None:
                        break

                    # add the speed to list
                    speed.append( nextNode.get_text())    

        self.spd = speed

    def get_basespeed(self , rank):

        # if rank is blank (default) use rank 0
        if rank == '':
            return self.spd[0]

        val = RANKS[rank]

        # return speed for the selected rank
        return self.spd[val]

    def update_speed(self , val ,base,  index  , teamspeed = False): 

        # replace the , with nothing to avoid errors
        base_Spd = base.replace(',' , '')        

        # value = 0 to avoid errors
        value = 0

        # checks if it's teamspead or normal speed rune
        if val == 'None':
            self.percent[index] = 0

        elif teamspeed:
            value = TEAM_SPEED[val]
        else:
            value = SPEED[val] 

        # adds the rune value to percent value
        self.percent[index] = value

        # buff calculations below
        actual_percent = 0
        
        for i in self.percent:
            actual_percent += i

        new_spd = int(base_Spd)
        new_spd += actual_percent * new_spd
        round(new_spd)

        return int(new_spd)

    def update_speed_g(self , val , base):

        # read above
        base_Spd = base.replace(',' , '')

        value = RUNE_GUARDIAN[val]

        self.percent[10] = value

        # buff calculations below
        actual_percent = 0
        
        for i in self.percent:
            actual_percent += i

        new_spd = int(base_Spd)
        new_spd += actual_percent * new_spd
        round(new_spd)

        return int(new_spd)


@app.route('/')
def my_form():

    # returns main template
    return render_template("index.html"  , title=title ,speed=SPEED.keys() , tspeed=TEAM_SPEED.keys() , ranks=RANKS.keys() , guard=RUNE_GUARDIAN.keys() ,speed2=SPEED , rank=RANKS)

# a speed object
CLC = Speed()

@app.route('/fu', methods=['POST'])
def my_form_post():

    # a function called when the search button is clicked on 

    if request.method == 'POST':
        text = request.form['name']
        rank = request.form['rank']

        processed_text = str(text)

        CLC.get_speed(processed_text)

        return CLC.get_basespeed(rank)

    return render_template("index.html" , base_spd = 300)

@app.route('/on' ,  methods=['POST'])
def onchange():

    # a function called when a rune is selected 
    if request.method == 'POST':
        val = request.form['value']
        base = request.form['base']
        index = request.form['index']
        spd = 0

        if 'TEAM' in val:
           spd = CLC.update_speed(val , base,  int(index) ,True)
           return str(spd)
        else:
           spd = CLC.update_speed(val , base , int(index) )  
           return str(spd)
        

    return 200

@app.route('/rank_onchange' , methods=['POST'])  
def rank_onchange():

    # function called when rank is changed 

    if request.method == 'POST':
        rank = request.form['rank']

        return CLC.get_basespeed(rank)


@app.route('/gaurdian_onchange' , methods=['POST'])  
def gaurdian_onchange():

    # function when guardian percent is changed
    if request.method == 'POST':
        gaurd = request.form['gaurdian']
        base = request.form['base']

        spd = CLC.update_speed_g(gaurd , base)

        return str(spd)

    return 200

if __name__ == "__main__":
    app.run()