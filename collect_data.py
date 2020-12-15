import argparse
import csv
import os
from collections import defaultdict
from tqdm import tqdm
import openreview

def download_iclr(client, outdir='./', get_pdfs=False, year=2019):
    '''
    Main function for downloading ICLR metadata (and optionally, PDFs)
    '''
    # pylint: disable=too-many-locals

    print('getting metadata...')
    submissions = openreview.tools.iterget_notes(
        client, invitation=f'ICLR.cc/{year}/Conference/-/Blind_Submission')
    submissions_by_forum = {n.forum: n for n in submissions}

    
    # Because of the way the Program Chairs chose to run ICLR '19, there are no "decision notes";
    # instead, decisions are taken directly from Meta Reviews.
    meta_reviews = openreview.tools.iterget_notes(
        client, invitation=f'ICLR.cc/{year}/Conference/-/Paper.*/Meta_Review')
    meta_reviews_by_forum = {n.forum: n for n in meta_reviews}

    # Build a list of metadata.
    # For every paper (forum), get the review ratings, the decision, and the paper's content.
    metadata = []
    paper_id = 0
    for forum in submissions_by_forum:
        
        forum_meta_review = meta_reviews_by_forum[forum]
        decision = forum_meta_review.content['recommendation']

        tmp = submissions_by_forum[forum].content['authors']
        authors = []
        for author in tmp:
            first = author.split(' ')[0]
            last = author.split(' ')[-1]
            if last[-1] == '*':
                last = last[0:-1]
            authors.append(f'{first} {last}')
        authors = ', '.join(authors)

        forum_metadata = {
            'paper_id': paper_id,
            'authors': authors,
            'decision': decision,
        }
        metadata.append(forum_metadata)
        paper_id += 1

    print('writing metadata to file...')
    # write the metadata, one JSON per line:
    with open(os.path.join(outdir, f'iclr{year}_papers.csv'), 'w', newline='') as file_handle:
        fc = csv.DictWriter(file_handle, 
                            fieldnames=metadata[0].keys())
        fc.writeheader()
        fc.writerows(metadata)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--outdir', default='./', help='directory where data should be saved')

    parser.add_argument('--baseurl', default='https://api.openreview.net')
    parser.add_argument('--username', default='', help='defaults to empty string (guest user)')
    parser.add_argument('--password', default='', help='defaults to empty string (guest user)')
    parser.add_argument('--year', default=2019, help='defaults to 2019')

    args = parser.parse_args()

    outdir = args.outdir

    year = args.year

    client = openreview.Client(
        baseurl=args.baseurl,
        username=args.username,
        password=args.password)
    

    download_iclr(client, outdir, year=year)