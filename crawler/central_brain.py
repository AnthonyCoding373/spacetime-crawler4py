from threading import RLock
import sys

all_stop_words = {'a','able','about','above','abst','accordance','according','accordingly','across','act','actually','added','adj','affected','affecting','affects','after','afterwards','again','against','ah','all','almost','alone','along','already','also','although','always','am','among','amongst','an','and','announce','another','any','anybody','anyhow','anymore','anyone','anything','anyway','anyways','anywhere','apparently','approximately','are','aren','arent','arise','around','as','aside','ask','asking','at','auth','available','away','awfully','b','back','be','became','because','become','becomes','becoming','been','before','beforehand','begin','beginning','beginnings','begins','behind','being','believe','below','beside','besides','between','beyond','biol','both','brief','briefly','but','by','c','ca','came','can','cannot','can\'t','cause','causes','certain','certainly','co','com','come','comes','contain','containing','contains','could','couldnt','d','date','did','didn\'t','different','do','does','doesn\'t','doing','done','don\'t','down','downwards','due','during','e','each','ed','edu','effect','eg','eight','eighty','either','else','elsewhere','end','ending','enough','especially','et','et-al','etc','even','ever','every','everybody','everyone','everything','everywhere','ex','except','f','far','few','ff','fifth','first','five','fix','followed','following','follows','for','former','formerly','forth','found','four','from','further','furthermore','g','gave','get','gets','getting','give','given','gives','giving','go','goes','gone','got','gotten','h','had','happens','hardly','has','hasn\'t','have','haven\'t','having','he','hed','hence','her','here','hereafter','hereby','herein','heres','hereupon','hers','herself','hes','hi','hid','him','himself','his','hither','home','how','howbeit','however','hundred','i','id','ie','if','i\'ll','im','immediate','immediately','importance','important','in','inc','indeed','index','information','instead','into','invention','inward','is','isn\'t','it','itd','it\'ll','its','itself','i\'ve','j','just','k','keep keeps','kept','kg','km','know','known','knows','l','largely','last','lately','later','latter','latterly','least','less','lest','let','lets','like','liked','likely','line','little','\'ll','look','looking','looks','ltd','m','made','mainly','make','makes','many','may','maybe','me','mean','means','meantime','meanwhile','merely','mg','might','million','miss','ml','more','moreover','most','mostly','mr','mrs','much','mug','must','my','myself','n','na','name','namely','nay','nd','near','nearly','necessarily','necessary','need','needs','neither','never','nevertheless','new','next','nine','ninety','no','nobody','non','none','nonetheless','noone','nor','normally','nos','not','noted','nothing','now','nowhere','o','obtain','obtained','obviously','of','off','often','oh','ok','okay','old','omitted','on','once','one','ones','only','onto','or','ord','other','others','otherwise','ought','our','ours','ourselves','out','outside','over','overall','owing','own','p','page','pages','part','particular','particularly','past','per','perhaps','placed','please','plus','poorly','possible','possibly','potentially','pp','predominantly','present','previously','primarily','probably','promptly','proud','provides','put','q','que','quickly','quite','qv','r','ran','rather','rd','re','readily','really','recent','recently','ref','refs','regarding','regardless','regards','related','relatively','research','respectively','resulted','resulting','results','right','run','s','said','same','saw','say','saying','says','sec','section','see','seeing','seem','seemed','seeming','seems','seen','self','selves','sent','seven','several','shall','she','shed','she\'ll','shes','should','shouldn\'t','show','showed','shown','showns','shows','significant','significantly','similar','similarly','since','six','slightly','so','some','somebody','somehow','someone','somethan','something','sometime','sometimes','somewhat','somewhere','soon','sorry','specifically','specified','specify','specifying','still','stop','strongly','sub','substantially','successfully','such','sufficiently','suggest','sup','sure t','take','taken','taking','tell','tends','th','than','thank','thanks','thanx','that','that\'ll','thats','that\'ve','the','their','theirs','them','themselves','then','thence','there','thereafter','thereby','thered','therefore','therein','there\'ll','thereof','therere','theres','thereto','thereupon','there\'ve','these','they','theyd','they\'ll','theyre','they\'ve','think','this','those','thou','though','thoughh','thousand','throug','through','throughout','thru','thus','til','tip','to','together','too','took','toward','towards','tried','tries','truly','try','trying','ts','twice','two','u','un','under','unfortunately','unless','unlike','unlikely','until','unto','up','upon','ups','us','use','used','useful','usefully','usefulness','uses','using','usually','v','value','various','\'ve','very','via','viz','vol','vols','vs','w','want','wants','was','wasnt','way','we','wed','welcome','we\'ll','went','were','werent','we\'ve','what','whatever','what\'ll','whats','when','whence','whenever','where','whereafter','whereas','whereby','wherein','wheres','whereupon','wherever','whether','which','while','whim','whither','who','whod','whoever','whole','who\'ll','whom','whomever','whos','whose','why','widely','willing','wish','with','within','without','wont','words','world','would','wouldnt','www','x','y','yes','yet','you','youd','you\'ll','your','youre','yours','yourself','yourselves','you\'ve','z','zero'
}

class StoredData:
    def __init__(self):
        self.lock = RLock()
        self.num_of_uniqueURL = set()
        self.most_common_words = {}
        self.most_frequent_words = {}
        self.longestpage = "Does not Exist"
        self.longest_page_word_count = 0
        self.subdomain = {}  
        self.count = 0

    def alter_unique_URL(self, url):
        self.num_of_uniqueURL.add(url)
    
    def alter_most_common_words(self, words):
        for text in words:
            text = text.lower()
            if text not in all_stop_words:
                if text not in self.most_common_words:
                    self.most_common_words[text] = 1 
                else:
                    self.most_common_words[text] = self.most_common_words[text] + 1
    
    def alter_longest_page(self, url, number_of_words):
        if number_of_words > self.longest_page_word_count:
                self.longest_page_word_count = number_of_words
                self.longestpage = url

    def alter_subdomains(self, current_subdomain):
        if current_subdomain not in self.subdomain:
            self.subdomain[current_subdomain] = 1
        else:
            self.subdomain[current_subdomain] = self.subdomain[current_subdomain] + 1

    def alter_data(self, trnum_of_uniqueURL, trmost_common_words, trmost_frequent_words, trlongestpage, trlongest_page_word_count, trsubdomain):
        for i in trnum_of_uniqueURL:
            self.num_of_uniqueURL.add(i)
        
        for i in trmost_common_words.keys():
            if i not in all_stop_words:
                if i not in self.most_common_words:
                    self.most_common_words[i] = trmost_common_words[i] 
                else:
                    self.most_common_words[i] = self.most_common_words[i] + trmost_common_words[i] 

        if trlongest_page_word_count > self.longest_page_word_count:
            self.longest_page_word_count = trlongest_page_word_count
            self.longestpage = trlongestpage
        
        for i in trsubdomain.keys():
            if i not in self.subdomain:
                self.subdomain[i] = trsubdomain[i] 
            else:
                self.subdomain[i] = self.subdomain[i] + trsubdomain[i] 

        self.count = self.count + 1
        #print("COUTN: ", self.count)
        if self.count > 100:
            self.count = 0
            self.store_in_file()


    def print_brain_data(self):
        print("CHECKING DATA:                      ")
        print("Number of uniqueURLS: ", len(self.num_of_uniqueURL))
        print("Longest page: " + self.longestpage)
        print("Longest page contains ", self.longest_page_word_count, " words")
        self.most_frequent_words = dict(sorted(self.most_common_words.items(), key=lambda item: item[1], reverse=True))
        print("All most common words sorted by frequency: ")
        #print(self.most_frequent_words.keys())
        print(list(self.most_frequent_words.keys())[:51])
        print("All Detected Subdomains: ")
        for item in self.subdomain:
            print(item, self.subdomain[item])

    def store_in_file(self):
        with open("general-log.txt", 'w') as file:
            file.write(f"Number of unique URLS: {len(self.num_of_uniqueURL)} \n")
            file.write(f"Longest Page: {self.longestpage} \n")
            file.write(f"Longest Page contains: {self.longest_page_word_count} words\n")

            file.write("50 Most common Words:\n")
            #print("All words are:", self.most_common_words)
            self.most_frequent_words = dict(sorted(self.most_common_words.items(), key=lambda item: item[1], reverse=True))
            for word in list(self.most_frequent_words.keys())[:50]:
                file.write(f"  {word}\n")

            file.write("Unique Subdomains: \n")
            for item in self.subdomain.keys():
                file.write(f"  {item}: {self.subdomain[item]}\n")

    def debug_test(self):
        print("Num of unique URLS: ", len(self.num_of_uniqueURL))