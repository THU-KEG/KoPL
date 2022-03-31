

知识库下载
=====================================================================================================================================================================================
我们从Wikidata中抽取了一个高质量的稠密子集 `Wikidata15k <https://cloud.tsinghua.edu.cn/f/ea83c57d262b4a09ab92/?dl=1>`_，包含794个
概念，16,960个实体，363个
关系，846个
属性。以下的样例都基于这个知识库。


schema展示（部分）
=====================================================================================================================================================================================
================================================== ============================================= =============================================
概念                                               关系                                           属性
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

简单问答
====================================================================================================================================================

查询属性
----------------------------------------------------------------
.. glossary::

    查询例句：When did the 1985 Major League Baseball season take place?
    例句释义：1985年美国职业棒球大联盟赛季是什么时候开始的？
    查询结果：1985
    .. image:: demo1.png

        
::

    engine.QueryAttr(
        engine.Find("1985 Major League Baseball season"),
        "point in time"
    )

查询在修饰符限定下的属性
----------------------------------------------------------------
.. glossary::

    查询例句：When was Oscar and Lucinda published in Germany?
    例句释义：Oscar and Lucinda什么时候在德国公映的？
    查询结果：1998-06-25
    .. image:: demo2.png

        
::

    engine.QueryAttrUnderCondition(
        engine.Find("Oscar and Lucinda"),
        "publication date",
        "place of publication",
        "Germany"
    )

查询属性的修饰值
----------------------------------------------------------------
.. glossary::

    查询例句：When did Will & Grace have 8 seasons?
    例句释义：Will & Grace什么时候有了第8季？
    查询结果：2006-05-18
    .. image:: demo3.png

        
::

    engine.QueryAttrQualifier(
        engine.Find("Will & Grace"),
        "number of seasons",
        "8",
        "point in time"
    )

查询关系
----------------------------------------------------------------
.. glossary::
    
    查询例句：How is Viggo Mortensen releated to the 10th Screen Actors Guild Awards?
    例句释义：Viggo Mortensen和第十届银幕演员协会奖是什么关系？
    查询结果：award received
    .. image:: demo4.png

        
::

    engine.QueryRelation(
        engine.Find("Viggo Mortensen"),
        engine.Find("10th Screen Actors Guild Awards")
    )

查询关系的修饰值
----------------------------------------------------------------
.. glossary::

    查询例句：When did Mitchell Hurwitz end his education at Georgetown University?
    例句释义：Mitchell Hurwitz什么时候结束了在乔治敦大学的学业？
    查询结果：1985
    .. image:: demo5.png

        
::

    engine.QueryRelationQualifier(
        engine.Find("Mitchell Hurwitz"),
        engine.Find("Georgetown University"),
        "educated at",
        "end time"
    )

复杂问答
====================================================================================================================================================
多跳查询
----------------------------------------------------------------
.. glossary::

    查询例句：How many industry computer languages are related to UNIX?
    例句释义：有多少种工业计算机语言与UNIX相关？？
    查询结果：22
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

    查询例句：Who is known for the new wave of European origin?
    例句释义：谁因欧洲起源的新浪潮而闻名？
    查询结果：Gary Numan
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

比较
----------------------------------------------------------------
.. glossary::

    查询例句：Which show produced by Dreamworks is the longest?
    例句释义：梦工厂制作的哪个节目最长？
    查询结果：Into the West
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

    查询例句：Who is taller, Kobe Bryant or LeBron James?
    例句释义：谁更高，Kobe Bryant 还是 LeBron James?
    查询结果：LeBron James
    .. image:: demo9.png

        
::

    engine.SelectBetween(
        engine.Find("Kobe Bryant"),
        engine.Find("LeBron James"),
        "height",
        "greater"
    )

逻辑操作
----------------------------------------------------------------    
.. glossary::

    查询例句：What feature film was nominated for an Academy Award for Best Supporting Actor and an Academy Award for Best Actor?
<<<<<<< HEAD
    哪部故事片获得奥斯卡最佳男配角奖和最佳男主角奖提名？
    查询结果：Fiddler on the Roof
    .. image:: demo10.png
=======
    例句释义：哪部故事片获得奥斯卡最佳男配角奖和最佳男主角奖提名？
    查询结果：Fiddler on the Roof, Pirates of the Caribbean: The Curse of the Black Pearl, The Straight Story
>>>>>>> 5688cef5c141387c80afe169d29346d3ac7f3963

        
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

    查询例句：How many symptoms indicate lung cancer or have obesity as a risk factor?
    例句释义：有多少症状表明肺癌或肥胖是危险因素？
    查询结果：4
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

事实验证
----------------------------------------------------------------    
.. glossary::

    查询例句：Are there less than 30000 households on the date 2011-01-01 in the big city that is an administrative division of North Brabant?
    例句释义：在2011年1月1日，北布拉班特行政区的大城市的住户是否少于30000户？
    查询结果：yes
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

    查询例句：Did the television series titled All in the Family start on 1971-01-12?
    例句释义：这部名为《All in the Family》的电视连续剧是从1971年1月12日开始的吗？
    查询结果：yes
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
