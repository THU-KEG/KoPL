

How to download knowledge base
=====================================================================================================================================================================================
We extract a high quality dense subset from Wikidata named `Wikidata15k <https://cloud.tsinghua.edu.cn/f/ea83c57d262b4a09ab92/?dl=1>`_, which contains 794 concepts, 16,960 entities, 363 relations and 846 attributes. The following examples are all based on this subset.


schema (partial)
=====================================================================================================================================================================================
================================================== ============================================= =============================================
Concept                                               Relation                                           Attribute
================================================== ============================================= =============================================
human                                              occupation                                    point in time                                
film                                               country                                       determination method                         
association football club                          genre                                         statement is subject of                      
city of the United States                          ethnic group                                  review score by                              
city                                               record label                                  ranking                                      
university                                         sport                                         for work                                     
television series                                  composer                                      population                                   
administrative territorial entity                  screenwriter                                  start time                                   
video game                                         voice actor                                   end time                                     
business                                           cause of death                                nominal GDP                                  
sovereign state                                    religion                                      official website                             
organization                                       manner of death                               points for                                   
record label                                       capital                                       ISNI                                         
band                                               has part                                      nominee                                      
television film                                    color                                         publication date                             
award                                              military branch                               demonym                                      
national association football team                 industry                                      date of birth                                
town                                               author                                        inflation rate                               
written work                                       eye color                                     inception                                    
public university                                  currency                                      character role                               
animated feature film                              family name                                   applies to part                              
rock band                                          academic degree                               language of work or name                     
music genre                                        head of government                            winner                                       
big city                                           political ideology                            postal code                                  
Academy Awards ceremony                            military rank                                 life expectancy                              
disease                                            programming language                          title                                        
film production company                            heritage designation                          number of points/goals/set scored            
political party                                    operating system                              total fertility rate                         
profession                                         programming paradigm                          number of matches played/races/starts        
feature film                                       soundtrack album                              place of publication                         
first-level administrative country subdivision     family                                        Twitter username                             
sports season                                      chief executive officer                       duration                                     
miniseries                                         architectural style                           area                                         
video game developer                               mountain range                                number of subscribers                        
ethnic group                                       diaspora                                      official name                                
state of the United States                         republic                                      Human Development Index                      
land-grant university                              drama film                                    date of death                                
geographic region                                  forward                                       name in native language                      
award ceremony                                     violin                                        number of out-of-school children             
capital                                            marriage                                      country                                      
ice hockey team                                    experimental music                            local dialing code                           
county of New York                                 Christianity                                  elevation above sea level                    
language                                           television                                    CANTIC-ID                                    
war                                                historical period drama                       birth name                                   
baseball team                                      running back                                  work period (start)                          
legislative term                                   prime minister                                native label                                 
county of California                               drum                                          Instagram username                           
ceremonial county of England                       action film                                   Dewey Decimal Classification                 
American football team                             guitar                                        short name                                   
county of Pennsylvania                             synthesizer                                   Munzinger IBA                                
literary award                                     male organism                                 diplomatic mission sent                      
basketball team                                    computer science                              SPLASH                                       
private university                                 special effects                               Libris-URI                                   
type of sport                                      actor                                         subreddit                                    
chemical compound                                  video game                                    series ordinal                               
television station                                 English                                       located at street address (DEPRECATED)       
republic                                           comedy                                        located at street address                    
animated series                                    vice president                                located in the administrative territorial entity
film series                                        cult film                                     FIPS 10-4 (countries and regions)            
class of instruments                               politics                                      motto text                                   
Grammy Award                                       reggae                                        number of children                           
island                                             engineering                                   pronunciation audio                          
single                                             alternative rock                              FIPS 6-4 (US counties)                       
animated film                                      piano                                         nickname                                     
class of award                                     democracy                                     licence plate code                           
county of Ohio                                     secretary of state                            height                                       
activity                                           president                                     ISO 3166-2 code                              
album                                              writer                                        cost                                         
historical country                                 biography                                     box office                                   
academic discipline                                film                                          acquisition transaction                      
film award                                         rock and roll                                 number of episodes                           
superhero                                          judge                                         instance of                                  
television series episode                          pop rock                                      WOEID                                        
Summer Olympic Games                               scientist                                     PermID                                       
Primetime Emmy Award                               Southern rock                                 British Museum person-institution            
Academy Awards                                     Islam                                         pseudonym                                    
industry                                           jazz                                          academic major                               
occupation                                         keyboard instrument                           number of seasons                            
literary work                                      announcer                                     object has role                              
college of the University of Oxford                crime fiction                                 patronage                                    
state of India                                     progressive rock                              exploitation visa number                     
town of the United States                          pop music                                     NUTS code                                    
independent city                                   bass guitar                                   academic degree                              
law school                                         LGBT                                          mass                                         
liberal arts college                               steel guitar                                  Deutsche Synchronkartei actor-ID             
college                                            bass                                          employees                                    
short film                                         adventure film                                dissolved, abolished or demolished           
film genre                                         thriller                                      direction relative to location               
college of the University of Cambridge             musician                                      number of speakers                           
county of New Jersey                               jam band                                      IPv4 routing prefix                          
constituency of the Rajya Sabha                    opera                                         Nintendo GameID                              
county of Florida                                  governor                                      students count                               
neighborhood                                       fantasy                                       TOID                                         
unitary state                                      artist                                        maritime identification digits               
county of Ireland                                  Protestantism                                 Giphy username                               
county of Illinois                                 electric piano                                country calling code                         
film festival edition                              businessperson                                UMLS CUI                                     
musical                                            model                                         frequency                                    
region of Italy                                    science fiction                               mains voltage                                
MTV Video Music Award                              documentary film                              ISO 3166-1 alpha-3 code                      
================================================== ============================================= =============================================

Simple question answering
====================================================================================================================================================

Query attribute
----------------------------------------------------------------
.. glossary::

    Question：When did the 1985 Major League Baseball season take place?
    Answer：1985
    .. image:: demo1.png

        
::

    engine.QueryAttr(
        engine.Find("1985 Major League Baseball season"),
        "point in time"
    )

Query attribute under qualifiers
----------------------------------------------------------------
.. glossary::

    Question：When was Oscar and Lucinda published in Germany?
    Answer：1998-06-25
    .. image:: demo2.png

        
::

    engine.QueryAttrUnderCondition(
        engine.Find("Oscar and Lucinda"),
        "publication date",
        "place of publication",
        "Germany"
    )

Query the qualifiers of the attribute
----------------------------------------------------------------
.. glossary::

    Question：When did Will & Grace have 8 seasons?
    Answer：2006-05-18
    .. image:: demo3.png

        
::

    engine.QueryAttrQualifier(
        engine.Find("Will & Grace"),
        "number of seasons",
        "8",
        "point in time"
    )

Query relation
----------------------------------------------------------------
.. glossary::
    
    Question：How is Viggo Mortensen releated to the 10th Screen Actors Guild Awards?
    Answer：award received
    .. image:: demo4.png

        
::

    engine.QueryRelation(
        engine.Find("Viggo Mortensen"),
        engine.Find("10th Screen Actors Guild Awards")
    )

Query the qualifiers of the relation
----------------------------------------------------------------
.. glossary::

    Question：When did Mitchell Hurwitz end his education at Georgetown University?
    Answer：1985
    .. image:: demo5.png

        
::

    engine.QueryRelationQualifier(
        engine.Find("Mitchell Hurwitz"),
        engine.Find("Georgetown University"),
        "educated at",
        "end time"
    )

Complex question answering
====================================================================================================================================================
Multi-hop query
----------------------------------------------------------------
.. glossary::

    Question：How many industry computer languages are related to UNIX?
    Answer：22
    .. image:: demo6.png

        
::

    engine.Count(
        engine.FilterConcept(
            engine.Relate(
                engine.FilterConcept(
                    engine.Relate(
                        engine.Find("Unix"),
                        "relative",
                        "backward"
                    ),
                    "industry"
                ),
                "language of work or name",
                "forward"
            ),
            "programming language"
        )
    )

.. glossary::

    Question：Who is known for the new wave of European origin?
    Answer：Gary Numan
    .. image:: demo7.png

        
::

    engine.QueryName(
        engine.FilterConcept(
            engine.Relate(
                engine.FilterConcept(
                    engine.Relate(
                        engine.Find("Europe"),
                        "country of origin",
                        "backward"
                    ),
                    "new wave"
                ),
                "famous people",
                "forward"
            ),
            "human"
        )
    )

Comparison
----------------------------------------------------------------
.. glossary::

    Question：Which show produced by Dreamworks is the longest?
    Answer：Into the West
    .. image:: demo8.png

        
::

    engine.SelectAmong(
            engine.FilterConcept(
                engine.Relate(
                    engine.Find("DreamWorks"),
                    "production company",
                    "backward"
                ),
                "miniseries"
            ),
            "duration",
            "largest"
        )

.. glossary::

    Question：Who is taller, Kobe Bryant or LeBron James?
    Answer：LeBron James
    .. image:: demo9.png

        
::

    engine.SelectBetween(
        engine.Find("Kobe Bryant"),
        engine.Find("LeBron James"),
        "height",
        "greater"
    )

Logical operations
----------------------------------------------------------------    
.. glossary::

    Question：What feature film was nominated for an Academy Award for Best Supporting Actor and an Academy Award for Best Actor?
    Answer：Fiddler on the Roof
    .. image:: demo10.png
        

::

    engine.QueryName(
        engine.And(
            engine.FilterConcept(
                engine.Relate(
                    engine.Find("Academy Award for Best Supporting Actor"),
                    "nominated for",
                    "backward"
                ),
                "feature film"
            ),
            engine.FilterConcept(
                engine.Relate(
                    engine.Find("Academy Award for Best Actor"),
                    "nominated for",
                    "backward"
                ),
                "feature film"
            )
        )
    )

.. glossary::

    Question：How many symptoms indicate lung cancer or have obesity as a risk factor?
    Answer：4
    .. image:: demo11.png

        
::

    engine.Count(
        engine.Or(
            engine.FilterConcept(
                engine.Relate(
                    engine.Find("lung cancer"),
                    "symptoms",
                    "forward"
                ),
                "symptom"
            ),
            engine.FilterConcept(
                engine.Relate(
                    engine.Find("obesity"),
                    "risk factor",
                    "forward"
                ),
                "symptom"
            )
        )
    )

Fact verification
----------------------------------------------------------------    
.. glossary::

    Question：Are there less than 30000 households on the date 2011-01-01 in the big city that is an administrative division of North Brabant?
    Answer：yes
    .. image:: demo12.png

        
::

    engine.VerifyDate(      
        engine.QueryAttrUnderCondition(      
            engine.FilterConcept(      
                    engine.Relate(      
                            engine.Find("North Brabant"),      
                            "contains administrative territorial entity",      
                            "forward"      
                    ),      
                    "big city"      
            ),      
            "number of households",      
            "point in time",      
            "2011"      
        ),      
        "30000",      
        "<"      
    )

.. glossary::

    Question：Did the television series titled All in the Family start on 1971-01-12?
    Answer：yes
    .. image:: demo13.png

        
::

    engine.VerifyDate(
        engine.QueryAttr(
            engine.FilterConcept(
                engine.FilterStr(
                    engine.FindAll(),
                    "title",
                    "All in the Family"
                ),
                "television series"
            ),
            "start time"
        ),
        "1971-01-12",
        "="
    )
