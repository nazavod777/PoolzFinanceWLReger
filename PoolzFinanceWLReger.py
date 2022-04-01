from web3 import Web3
from eth_account import Account
from threading import Thread, active_count
from msvcrt import getch
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from requests import get
from json import loads


class WrongResponse(Exception):
	def __init__(self, message):
		super().__init__(f'Wrong response, code: {str(message.status_code)}, response: {str(message.text)}')


disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('poolz.finance WL Auto Reger | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


while True:
	try:
		r = get('https://admin.poolz.finance/poolz-idos')

		if r.status_code != 200:
			raise WrongResponse(r)

		events = {list['name']:list['signUpId'] for list in loads(r.text)}

		for i in range(len(events.keys())):
			print(f"{str(i + 1)}. {list(events.keys())[i]}")
	
	except WrongResponse as error:
		logger.error(str(error))

	except Exception as error:
		logger.error(f'Unexpected error when getting events: {str(error)}')

	else:
		break

event_num = int(input('Enter event number: '))
event_id = int(events[list(events.keys())[event_num - 1]])

addresses_folder = str(input('\nTXT with Accounts (address:privatekey // privatekey:address // privatekey): '))
wait_tx_result = str(input('Wait TX result?: ')).lower()
threads = int(input('Threads: '))


with open (addresses_folder, 'r') as file:
	addresses = [row.strip() for row in file]


class WrongAddressFormat(Exception):
	def __init__(self, message):
		super().__init__(f'Wrong string format: {message}')



def mainth(wallet_data_file):

	try:
		if ':' in wallet_data_file:
			split_wallet_data = wallet_data_file.split(':')

			for current_wallet_data in split_wallet_data:
				if len(current_wallet_data) == 66 or len(current_wallet_data) == 64:

					if len(current_wallet_data) == 64:
						current_wallet_data == f'0x{current_wallet_data}'
					
					private_key == current_wallet_data

					break

			raise WrongAddressFormat(wallet_data_file)

		elif len(wallet_data_file) == 66 or len(wallet_data_file) == 64:
			if wallet_data_file[:2] != '0x':
				wallet_data_file = f'0x{wallet_data_file}'

			private_key = wallet_data_file

		else:
			raise WrongAddressFormat(wallet_data_file)

		wallet_data = Account.from_key(private_key)

		transaction = contract.functions.SignUp(event_id).buildTransaction({
					'gas': 40906,
					'gasPrice': web3.toWei('5', 'gwei'),
					'from': Web3.toChecksumAddress(wallet_data.address),
					'nonce': web3.eth.get_transaction_count(Web3.toChecksumAddress(wallet_data.address)),
					'value': web3.toWei(5441742300, 'mwei')
					})


		signed_txn = web3.eth.account.signTransaction(transaction, private_key=wallet_data.privateKey.hex())
		tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
		logger.info(f'[{wallet_data.address}] TX id: {web3.toHex(tx_hash)}')

		if wait_tx_result == 'y':
			txstatus = web3.eth.waitForTransactionReceipt(tx_hash).status

			if txstatus == 1:
				logger.success(f'[{wallet_data.address}] TX status: {txstatus}')

			else:
				logger.error(f'[{wallet_data.address}] TX status: {txstatus}')


	except ValueError as error:
		logger.error(f'[{wallet_data.address}] ValueError: {str(error)}')

		with open('error.txt', 'a') as file:
			file.write(f'{wallet_data_file}\n')
	
	except WrongAddressFormat as error:
		logger.error(f'[{wallet_data.address}] Wrong address format: {str(error)}')

	except Exception as error:
		logger.error(f'[{wallet_data.address}] Unexpected error: {str(error)}')

		with open('error.txt', 'a') as file:
			file.write(f'{wallet_data_file}\n')

	else:
		logger.success(f'[{wallet_data.address}] the work was successfully completed')


if __name__ == '__main__':

	clear()

	web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
	abi = open('ABI','r').read().replace('\n','')
	contract = web3.eth.contract(address=Web3.toChecksumAddress('0x41b56bF3b21C53F6394a44A2ff84f1d2bBC27841'), abi=abi)


	while addresses:
		if active_count()-1 < threads:
			Thread(target=mainth, args = (addresses.pop(0), )).start()

	while active_count()-1 != 0:
		pass


	logger.success('Work completed successfully')
	print('\nPress Any Key To Exit...')
	getch()
	exit()