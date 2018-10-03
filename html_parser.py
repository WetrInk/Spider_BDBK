from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin 

# with python 3.x

class HtmlParser(object):
    
    def get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"/item/")) # match "/item/" 
        for link in links:
            new_url = link['href']
            new_full_url = urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def get_new_data(self, page_url, soup):
        """Get new data with BS4."""
        res_data = {} # a dict to save data. 

        # url
        res_data['url'] = page_url

        # title
        """
        <dd class="lemmaWgt-lemmaTitle-title">
        <h1>Python</h1>
        <h2>（计算机程序设计语言）</h2>
        <a href="javascript:;" class="edit-lemma cmn-btn-hover-blue cmn-btn-28 j-edit-link" style="display: inline-block;"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_edit-lemma"></em>编辑</a>
        <a class="lock-lemma" nslog-type="10003105" target="_blank" href="/view/10812319.htm" title="锁定"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_lock-lemma"></em>锁定</a>
        </dd>
        """
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title")
        print(title_node.h1)
        print(title_node.h2)
        if title_node.h2 is not None:
            res_data['title'] = title_node.h1.string + title_node.h2.string  
        elif title_node.h1 is not None:
            res_data['title'] = title_node.h1.string
        # improved the disambiguation
        print("TITLE >> ", res_data['title'])
        
        # data / summary
        """ <div class="para" label-module="para">Python 是一门有条理的和强大的面向对象的程序设计语言，类似于Perl, Ruby, Scheme, Java.</div> """

        summary_node = soup.find('div', class_="lemma-summary")
        res_data['data'] = summary_node.get_text()

        return res_data
    
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self.get_new_urls(page_url, soup)
        new_data = self.get_new_data(page_url, soup)
        return new_urls, new_data
