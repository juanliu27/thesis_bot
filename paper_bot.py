import arxiv
import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header

# 1. search
def get_papers():
    keywords = '("ai governance" OR "ai policy" OR "ai risk" OR "ai ethics" OR "ai benchmark")'
    search = arxiv.Search(
        query=keywords,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    results = []
    for r in search.results():
        results.append(f"【{r.title}】\n链接: {r.pdf_url}\n摘要: {r.summary[:200]}...")
    return "\n\n---\n\n".join(results)

# 2. email
def send_email(content):

    sender = os.environ['EMAIL_SENDER']
    password = os.environ['EMAIL_PASSWORD']
    receiver = os.environ['EMAIL_RECEIVER']
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header('🤖 今日AI治理-论文日报', 'utf-8')

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
        server.quit()
        print("Success!")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    paper_content = get_papers()
    if paper_content:
        send_email(paper_content)
