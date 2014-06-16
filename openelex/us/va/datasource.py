"""
Standardize names of VA source data files.

To run mappings from invoke task:

    invoke datasource.mappings -s VA

"""
import re

from openelex.api import elections as elec_api
from openelex.base.datasource import BaseDatasource


class Datasource(BaseDatasource):

    #base_url = "http://www.elections.state.md.us/elections/%(year)s/election_data/"

    # PUBLIC INTERFACE
    def mappings(self, year=None):
        """Return array of dicts  containing source url and 
        standardized filename for raw results file, along 
        with other pieces of metadata
        """
        mappings = []
        for yr, elecs in self.elections(year).items():
            mappings.extend(self._build_metadata(yr, elecs))
        return mappings

    def target_urls(self, year=None):
        "Get list of source data urls, optionally filtered by year"
        return [item['raw_url'] for item in self.mappings(year)]

    def filename_url_pairs(self, year=None):
        return [(item['generated_filename'], item['raw_url']) 
                for item in self.mappings(year)]

    # PRIVATE METHODS
    def _build_metadata(self, year, elections):
        meta = []
        for election in elections:
            for link in election['direct_links']:
                filename_bits = (
                    election['start_date'].replace('-',''),
                    self.state,
                    self._race_type(election, link),
                    'precinct.csv',
                )
                meta.append({
                    "generated_filename": "__".join(filename_bits),
                    "raw_url": link,
                    "ocd_id": 'ocd-division/country:us/state:va',
                    "name": 'Virginia',
                    "election": election['slug']
                })
        return meta

    def _race_type(self, election, source_link):
        #if election['slug'] == 'va-2014-01-07-special-general':
        #    import ipdb;ipdb.set_trace()
        rtype = election['race_type']
        if 'primary' in rtype:
            party = re.search(r'(Democratic|Republican)', source_link, re.I).groups()[0].lower()
            race_name = "%s__%s" % (party, rtype)
        else:
            race_name = rtype
        if election['special']:
            race_name = 'special__%s' % race_name
        return race_name.replace('-', '_')
