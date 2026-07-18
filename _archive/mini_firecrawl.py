import paramiko,socket,time
a=socket.getaddrinfo("118.89.111.224",22,2,1)[0][4]
s=socket.socket(2,1);s.settimeout(8);s.connect(a)
t=paramiko.Transport(s);t.start_client();t.auth_password("ubuntu","YOUR_PASSWORD")

# Install lightweight scraper
c=t.open_session()
c.exec_command("pip3 install requests beautifulsoup4 markdownify -i https://pypi.tuna.tsinghua.edu.cn/simple --break-system-packages 2>&1 | tail -2")
time.sleep(20)
print("Install:", c.recv(4096).decode()[:200])

# Write scraper
scraper="""#!/usr/bin/env python3
# Mini Firecrawl - Web to Markdown
import requests,sys,re
from bs4 import BeautifulSoup
from markdownify import markdownify as md

url=sys.argv[1] if len(sys.argv)>1 else 'https://example.com'
headers={'User-Agent':'Mozilla/5.0'}
r=requests.get(url,headers=headers,timeout=15)
soup=BeautifulSoup(r.text,'html.parser')

# Remove noise
for tag in soup(['script','style','nav','footer','header','aside']):
    tag.decompose()

# Get main content
body=soup.find('body') or soup
text=md(str(body),heading_style='ATX').strip()

# Clean up
text=re.sub(r'\\n{3,}','\\n\\n',text)
print(text[:5000])
"""
c2=t.open_session()
c2.exec_command(f'cat > /home/ubuntu/mini_firecrawl.py << \'PYEOF\'\n{scraper}\nPYEOF\nchmod +x /home/ubuntu/mini_firecrawl.py')
time.sleep(3)

# Test it
c3=t.open_session()
c3.exec_command("python3 /home/ubuntu/mini_firecrawl.py https://example.com 2>&1 | head -30")
time.sleep(10)
print("Test:", c3.recv(4096).decode()[:500])

c.close();c2.close();c3.close();t.close()
