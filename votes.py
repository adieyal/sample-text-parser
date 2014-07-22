import sys
"""
Sample code that parses a hansard and extracts parliamentary votes (well only the AYES)
run it as follows python votes.py 2012-01-18_104745_1.doc.txt

for instance, it will pull out all the AYES that you can find on line 694 of 2012-01-18_104745_1.doc.txt

"""

class Scraper(object):
    SKIP = "skip"

    def __init__(self):
        self._reset()

    def _reset(self):
        self.state = self.state_divided
        self.ayes_buffer = ""

    def state_divided(self, line):
        if "The House divided" in line:
            self.state = self.state_find_ayes

    def state_find_ayes(self, line):
        if "AYES" in line:
            self.state = self.state_process_ayes
            return Scraper.SKIP

    def state_process_ayes(self, line):
        if line.strip() == "":
            vote =  self.ayes_buffer.split(":")[1].split(";")
            self.votes.append(vote)
            self._reset()
        else:
            self.ayes_buffer += line.strip()

    def scrape(self, fp):
        self._reset()
        self.votes = []
        for line in fp:
            while True:
                res = self.state(line)
                if res == Scraper.SKIP:
                    continue
                break
        return self.votes

def main():
    fp = open(sys.argv[1])
    scraper = Scraper()
    for vote in scraper.scrape(fp):
        print vote
    
if __name__ == "__main__":
    main()
