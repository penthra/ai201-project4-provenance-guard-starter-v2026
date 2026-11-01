"""Submit three saved style probes with the real detector; verify all labels.

Run: python verify_labels.py
Each run appends three decisions to logs/audit.jsonl.
The texts are synthetic reachability probes, not an authorship accuracy test.
"""
import json
from pathlib import Path

from app import app
import audit
import scoring


def main():
    root = Path(__file__).resolve().parent
    pieces = json.loads((root / 'results' / 'signal_comparison.json').read_text())
    expected = {
        'Plain conventional prose': 'unsure',
        'Varied narrative': 'human',
        'Repeated unusual vocabulary': 'ai',
    }
    print('Configured ranges:', scoring.label_ranges(), flush=True)
    rows = []
    client = app.test_client()
    for piece in pieces:
        response = client.post('/submit', json={
            'text': piece['text'], 'creator_id': 'label-coverage-check',
        })
        assert response.status_code == 200, response.get_json()
        body = response.get_json()
        assert body['guess'] == expected[piece['name']], body
        assert (body['guess'], body['label']) == scoring.score_to_label(body['confidence'])
        entry, = audit.entries_for(body['content_id'])
        for key in ('guess', 'label', 'model_score', 'style_score'):
            assert entry[key] == body[key]
        assert entry['combined_score'] == body['confidence']
        assert entry in client.get('/log').get_json()['entries']
        row = {'name': piece['name'], 'text': piece['text'], 'response': body}
        rows.append(row)
        print(json.dumps(row, ensure_ascii=True), flush=True)
    assert {row['response']['guess'] for row in rows} == {'human', 'unsure', 'ai'}
    output = root / 'results' / 'label_coverage.json'
    output.write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    print('PASS: all three labels reached through /submit and matched persisted audit records.')


if __name__ == '__main__':
    main()
