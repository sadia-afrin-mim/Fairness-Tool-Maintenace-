import csv
import requests
import time  

def search_github_issues_with_pagination(repo, keyword, auth_token):
    base_url = f"https://api.github.com/search/issues"
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {auth_token}'  
    }
    page = 1
    issues_retrieved = []

    while True:
        params = {
            'q': f"{keyword} repo:{repo}",
            'per_page': 100, 
            'page': page
        }

        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()  

            data = response.json()
            issues = data.get('items', [])
            if not issues:
                break  

            issues_retrieved.extend(issues)
            page += 1  

            remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
            if remaining < 10:  
                time.sleep(60)  
            else:
                time.sleep(2)  

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching issues for {repo}: {e}")
            break

        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        current_time = time.time()
        if current_time < reset_time:
            wait_time = reset_time - current_time
            print(f"Rate limit hit. Waiting for {wait_time} seconds.")
            time.sleep(wait_time)

    with open("issues_output.csv", 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Repository', 'Keyword', 'Title', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()  

        for issue in issues_retrieved:
            writer.writerow({
                'Repository': repo,
                'Keyword': keyword,
                'Title': issue['title'],
                'URL': issue['html_url']
            })

if __name__ == "__main__":
    auth_token = "fill by yourself"

    # List of repositories
    repositories = [
        "ayong8/FairSight",
        "KenSciResearch/fairMLHealth",
        "INSPIRED-GMU/fairkit-learn",
        "equialgo/fairness-in-ml",
        "AI-secure/DecodingTrust",
        "oracle/guardian-ai",
        "AI4LIFE-GROUP/OpenXAI",
        "cakiki/ml-fairness-validity",
        "google/ml-fairness-gym",
        "JohnSnowLabs/langtest",
        "kozodoi/fairness",
        "EthicalML/xai",
        "microsoft/responsible-ai-toolbox",
        "ashryaagr/Fairness.jl",
        "ModelOriented/fairmodels",
        "ResponsiblyAI/responsibly",
        "vanderschaarlab/synthcity",
        "thu-coai/cotk",
        "wearepal/EthicML",
        "Giskard-AI/giskard",
        "dccuchile/wefe",
        "microsoft/SafeNLP",
        "firmai/ml-fairness-framework",
        "aws/amazon-sagemaker-clarify",
        "IBM/inFairness",
        "pliang279/sent_debias",
        "deel-ai/influenciae",
        "credo-ai/credoai_lens",
        "matloff/EDFfair",
        "FairRankTune",
        "fairpan",
        "microsoft/responsible-ai-toolbox-genbit",
        "ClearExplanationsAI/CLEAR",
        "dbountouridis/siren",
        "mlr-org/mcboost",
        "cylynx/verifyml",
        "oracle-samples/automlx",
        "adebayoj/fairml",
        "columbia/fairtest",
        "FAIR4HEP/FAIR4HEP-Toolkit",
        "barcoopensource/vivaldy-ai-analysis-dashboard",
        "Teddyzander/FairR",
        "hannanabdul55/seldonian-fairness",
        "aida-ugent/fairret",
        "Telefonica/XAIoGraphs",
        "kamyabnazari/fair-energy-ai",
        "sethneel/GerryFair",
        "umang-garg21/Fair-MisGAIN",
        "martinetoering/Embetter",
        "brandeis-machine-learning/FairPy",
        "Facebook Fairness Flow",
        "dssg/aequitas",
        "cosmicBboy/themis-ml",
        "Trusted-AI/AIF360",
        "drivendataorg/deon",
        "fairlearn/fairlearn",
        "fat-forensics/fat-forensics",
        "meelgroup/justicia",
        "linkedin/LiFT",
        "pymetrics/audit-ai",
        "Tizpaz/Parfait-ML",
        "PAIR-code/what-if-tool"
    ]

    keywords = ['API Update', 'API', 'Endpoint', 'Integration', 'Backward Compatibility', 'Deprecation', 'Refactor', 'REST', 'Changelog', 'Library Update']

    for repo in repositories:
        for keyword in keywords:
            search_github_issues_with_pagination(repo, keyword, auth_token)
