import requests
from collections import defaultdict
import pandas as pd

API_KEY = 'FILL YOUR OWN API KEY'


class CurrentBalance:
    def __init__(self, address_lst):

        self.address_lst = self._isList(address_lst)
        self.chain_lst = {1: 'Ethereum', 56: 'BSC'}

    def _isList(self, data):

        if type(data) != list:
            raise ValueError("Please input a list.")

        else:
            return data

    def _getDate(self):
        url = f'https://api.covalenthq.com/v1/1/address/{self.address_lst[0]}/balances_v2/?key={API_KEY}'
        r = requests.get(url)
        updated_at = r.json()['data']['updated_at'][:10]
        updated_at = updated_at.split('-')
        updated_at = "".join(updated_at)
        return updated_at

    def _getTokens(self):

        dict_store = defaultdict(list)

        for wallet in self.address_lst:
            for chain in self.chain_lst.keys():
                counter = 10
                while counter < 10:
                    try:
                        url = f'https://api.covalenthq.com/v1/{chain}/address/{wallet}/balances_v2/?key={API_KEY}'
                        r = requests.get(url)
                        data = r.json()['data']['items']
                        break
                    except Exception:
                        counter+=1
                        continue

                for item in data:
                    if float(item['balance']) > 0:
                        dict_store['chain'].append(self.chain_lst[chain])
                        dict_store['contract_name'].append(
                            item['contract_name'])
                        dict_store['contract_ticker_symbol'].append(
                            item['contract_ticker_symbol'])
                        dict_store['contract_address'].append(
                            item['contract_address'])
                        dict_store['balanceTokens'].append(
                            float(item['balance'])/(10**float(item['contract_decimals'])))
                        dict_store['valueUSD'].append(float(item['quote']))

        df = pd.DataFrame.from_dict(dict_store)

        return df

    def _saveToCSV(self, df):

        date = self._getDate()
        df.to_csv(f'TokenBalances_{date}.csv')

    def getCurrentBalances(self):

        token_df = self._getTokens()
        token_df = token_df.groupby(
            ['chain', 'contract_name', 'contract_ticker_symbol', 'contract_address']).sum().reset_index()
        token_df = token_df.sort_values(
            'valueUSD', ascending=False).reset_index(drop=True)

        self._saveToCSV(token_df)
        return token_df
