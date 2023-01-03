import warnings

from bert_score import score
from evaluate import load
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, Integer,
                        MetaData, String, Table, Text, create_engine, inspect,
                        update)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

warnings.filterwarnings("ignore")

# call bertscore and compare two variables
def compare(text1, text2, language):
    # while len(text1) > len(text2):
    #     text2.append("")
    # while len(text1) < len(text2):
    #     text1.append("")
    
    return score(
        text1, text2, model_type="allenai/led-base-16384", rescale_with_baseline=True, lang=language
    )

# Connect to database
dbcon = create_engine(
    "sqlite:////Users/scottsyms/code/HeritageCanada/data/fish/sample2.db"
)

Base=declarative_base()


# Database access
metadata = MetaData()
source = Table("source", metadata, autoload=True, autoload_with=dbcon)
# Session = sessionmaker(bind=dbcon)
# session = Session()



# Get maximum value for the pairid column
max_pairid = dbcon.execute(
    select([source.c.pairid]).order_by(source.c.pairid.desc()).limit(1)
).fetchone()[0]
print(max_pairid)

# Iterate through all the unique pairids
for i in range(1, max_pairid):
    # Get all the rows with the same pairid
    results = dbcon.execute(
        select(
            [source.c.id, source.c.english, source.c.french, source.c.spanish]
        ).where(source.c.pairid == i)
    )

    # print number of rows in results
    data = results.fetchall()
    returnrows = len(data)

    # Iterate through all the rows in results

    if returnrows == 2:
        print("Return Rows: ", returnrows)

        rowcounter=1
        # Iterate through all the rows in results
        for row in data:
            # Get the english and french text
            print("Rowcounter: " , rowcounter)
            if rowcounter == 1:
                print("Rowcount = 1")
                english1 = row[1]
                french1 = row[2]
                spanish1 = row[3]
            else:
                print("Rowcount = 2")
                english2 = row[1]
                french2 = row[2]
                spanish2 = row[3]
            rowcounter += 1
            # Compare the two texts

        # print("Length of English: " , len(english1), len(english2))
        # print("Length of French: ", len(french1), len(french2))
        # print("Length of Spanish: ", len(spanish1), len(spanish2))    
        englishscore = compare([english1], [english2], "en")
        frenchscore = compare([french1], [french2], "fr")
        spanishscore = compare([spanish1], [spanish2], "es")
        englishscore = sum([x[0].item() for x in englishscore])/3
        frenchscore = sum([x[0].item() for x in frenchscore])/3
        spanishscore = sum([x[0].item() for x in spanishscore])/3

        print("English Score: ", englishscore)
        print("French Score: ", frenchscore)
        print("Spanish Score: ", spanishscore)

        stmt = source.update().values(bertscoreenglish=englishscore, bertscorefrench=frenchscore, bertscorespanish=spanishscore).where(source.c.pairid == i)
        dbcon.execute(stmt)

        


            # Compare the two texts

print("English: ", english1)
print ("French: ", french1)
print ("Spanish: ", spanish1)

print ("English: ", english2)
print ("French: ", french2)
print ("Spanish: ", spanish2)


        # Get the spanish text


    # Populate english, french, and spanish text variable

    # Update each score column with the like language comparisons


# Modify English
# result = dbcon.execute(select(
#     [source.c.id, source.c.english, source.c.french, source.c.spanish]).limit(5))


text1='''
After she obtained her AB, Key worked as an assistant in German and biology at Green Bay High School from 1894 to 1898.[13][14][15][16] She then attended the University of Chicago and was awarded her PhD in zoology in 1901.[9][11] She briefly remained at the University of Chicago as an assistant until 1902.[1] Afterwards she became the head of the German and Nature Study department at the New Mexico Normal University from 1903 to 1904.[17] After living in California for three years, she became a presiding teacher at Belmont College from 1907 to 1909.[12] She then became a professor of German and biology at Lombard college from 1909 to 1912[13][18] where she fostered Sewall Wright's interest in genetics.[19] They continued a correspondence throughout their lives.[20]
'''

text2='''
From 1912 to 1914, Key worked as a eugenics field worker at the Eugenics Record Office.[18][1] Afterwards, she worked briefly as an investigator at the Public Charities Association in Pennsylvania.[21] From 1914 to 1917, she was an education director at the Pennsylvania State Training School in Polk.[21] As part of her position, she gave a talk on feeble-mindedness.[22] She also completed her seminal work "Feeble-minded Citizens in Pennsylvania," which was used to recommend appropriation from the Pennsylvania state legislature to isolate feeble-minded women from the population to prevent the spread of feeble-mindedness.[23]

Later, Key worked as an archivist for three years.[21] From 1920 to 1925, she was the head of biology and eugenics research in the Race Betterment Foundation.[24] While there, she gave lectures[25] including topics "Hereditary and Human Fitness,"[26] "The Comparative effect on the Individual Heredity and Environment",[27] "Heredity and Personality",[28] "Are we better than our forefathers?",[29] "Our Friends, the Trees",[30] and "Heredity and Eugenics".[31] She spoke at the Battle Creek Garden Club on the importance of trees.
'''

fish =compare([text1], [text2])
print(fish)
print(fish[0].item())
