# Thapar Project Report Generator

Used to generate more than **100+ Reports** this is the source code of popular project hosted at https://tietprojgen.skullzbones.com.

Uses Latex + OpenAI's GPT 3.5 + Streamlit to automatically generate your end semester projects!

## What is this?
This is a tool where you can automatically generate a project-report, If you don't know what it is then basically a big big report file with sections like Abstract, introduction, background, methodology, conclusions, bibliography.. etc

It works by having user input their project description (in big text-boxes), They will have to add lot's of information and this tool will use GPT's to augment/rewrite them formally and automatically typeset into a created latex format! The generate final pdf will be downloaded by the user, additionally it will also send raw latex files for manual editing to user (in case they want to tweak something)

**This tool only supports end-semester project reports, but can easily be tweaked for other documents, like Capstone/thesis/etc**

## Why?
Students pursuing technical degree at Thapar University have this **project semester** where they have to intern at any institution/organization for 6 months and at the end *present their work* back to university! This work is usually presented in several medium like:
- **Project Report** - A 25-50 page report detailing your work and accomplishment
- **Poster** - A graphical A3 sheet diagrams to express your work in easy manner
- **Video + Presentation** - To establish goodwill among faculty and live present your work back in university!

It was in the months of June, when my intern was nearing an end and I knew I have to submit my work to university (that includes project report..)

Now for the *lazy me* who believe *technology* is the *key*, Writing/Styling a 25 page word document was out of question (C'mon, **Who the hell even uses docs in this era, We have latex for that :/**)

Plus this so called project report **needs to be formatted properly** (with fixed font sizes, margins, god-know-what styles), moreover I talked with my peers who mostly used GPTs to generate content and copy-paste into the given format.. Well when we were to use GPT's for the same, and just perform lot of manual work of typesetting, I though to myself

Why cannot the **technology can do that for Us**?

and guess what..? I was right, technology can do pretty much everything (just in the hands of jugaadu developer (and a lazy person)), Oh.. that's my profile, *sheesh*

So what next? I put up my goggles, prepared myself for a weekend of all-nighter, put my phone on silent and ignored all the friends to develop this godly tool (Which is now open-sourced!)

## Features
- **Automatic Content Generator:** It uses GPT3.5 to automatically generate and typeset relevant content
- **Proper formatting:** Generated report is always in proper format, with correct font-size/etc
- **Mail to user:** Generated report raw files will always be mailed back to user, in case they want to tweak anything
- **Interactive Frontend:**  Easy to use frontend with guidelines about mentioning all kind of inputs required with examples
- **Login/Signup System:** Integrated with login/signup and basic account management
- **Admin Panel:** Admin panel to view number of generated reports and short summary, while features like topping up user!
- **Credit System:** Uses credit system to prevent abuse, user can buy/earn credits on this platform, fully functional with working transactions
- **Referral System:** Integrated referral system to allow invite-only earnings of credit and promotion of tool
- **Feedback System:** Integrated feedback so user can report/express themselves, all is logged and a copy is sent to original developer through email!
- **Good Error Handling:** All errors are handled/reported, while generated report/logs are always sent back to user for proper debugging
- **Privacy First:** No data about project/input text boxes are ever stored, everything is kept confidential and is sent back to user! Only basic information like project name, company name, etc are stored for usage logs
- **HTTPS Enabled** Enabled HTTPS serving using nginx
- **Easy deployments** Docker scripts for one click deployment

## How it works?
- Uses base/template latex format with placeholders for different sections
- Uses promptflow/pipelined LLM's to generate different sections/text of report
- Generated content are replaced back to template and is compiled against user data
- All data, generated etc are mailed back to user
- Uses streamlit to quickly prototype frontend
- Simple Json database supports all user management and credit systems
- Uses SMTP to mail all the required data

## Installation

**Prerequisite**
- Install [latex](https://www.latex-project.org/get) (With medium-full package) to support compilation into pdf 
- Get OpenAI API keys (supporting atleast 3.5 turbo) - [Read article here](https://medium.com/@VaibhavTechDev/get-the-openai-api-key-a-step-by-step-guide-2112690ebb86)
- (Optional) Mail credentials in SMTP to support mail systems

then:

Clone this repository
```
$ git clone https://github.com/hari01584/llm-tietprojectgen
```

Get into clone repository
```
$ cd llm-tietprojectgen
```

Install required libraries/packages using pipelined
```
$ pip install -r requirements.txt
```

Change API keys to what you have brought, they are located in files *llm_executor/call_promptflow.py* and *utils/func.py*, Locate the text and change them!

Finally run the project using
```
streamlit run /app/⭐-Introduction.py --server.port 8501
```

or even better! Run all-in-one suite with SSL and Nginx supported using Docker:
```
docker compose up
```

(Note: For docker and https enabled, please place your ssl keys into directory *nginx/*, with filename *fullchain.pem* and *privkey.pem*)

## Looking for Long Term Contributors
As you can see, this is merely a proof-of-concept project with good success metrics, the code is dirty and our db is even just plain json files :), but with the recent traction and good feedback I saw from lot of friends, I believe this could be developed further into more refined platform for multiple type of reports/serving multiple universities!

I merely setup a base, and to show what can be possible.. and therefore **I urge you to explore more use-cases and extend/renovate this project as you see fit**, This is just the starting point of many amazing applications we can have, So keep hacking into it :)

With that being said, I am always up to discussing more interesting stuff/exploring what more could be done! So you can hit me up anytime and expect a great conversation ;)