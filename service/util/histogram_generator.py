import logging
from logging.config import fileConfig
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from datetime import datetime, date, timedelta
from peewee import JOIN
from service.data_sources.models import Stock, ArticleScore, Article, StockArticle

class HistogramGenerator(object):
    '''Generates histograms for one or more stocks.'''

    def __init__(self):
        '''Constructor'''

        # For logging, since Histogram generator isn't directly tied into StockNewsAnalyzer.
        fileConfig('logging_config.ini')

        self.logger = logging.getLogger()

        self.logger.info('HistogramGenerator Loaded.')

    def generate_histogram_for_stock(self,stock_ticker):
        '''Generates a histogram for the given Stock.
        
        NOTE: A stock needs to be analyzed by the StockNewsAnalyzer before a histogram will be generated for it.

        Arguments:
            stock_ticker {str} -- The Stock to generate the histogram for.
        '''

        stock = Stock.get_or_none(ticker=stock_ticker)

        if stock is not None:

            self.logger.info('Generating histogram for ' + stock.ticker)

            # Only gather the scores that were made today.
            scores = [article_score.score for article_score in ArticleScore.select().join(Article, JOIN.INNER).join(StockArticle, JOIN.INNER).where((StockArticle.stock_ticker == stock_ticker) & (Article.save_date == date.today().__str__()))]

            if len(scores) == 0: raise Exception('No scores from today for this Stock. Did you analyze it first with the StockNewsAnalyzer?')

            plt.hist(scores, bins=10, range=(-1,1),label='Scores ({})'.format(len(scores)))

            plt.suptitle(stock_ticker)

            plt.show()    

    def generate_histogram_for_stocks(self,stock_tickers):
        '''Generates a histogram for multiple Stocks at once.
        
        Arguments:
            stock_tickers {list} -- A list of str stock tickers to generate the histogram for.
        '''

        '''
        for each stock_ticker in stock_tickers,
        gather the associated Stock from the database,
        only saving it in the list if the returned Stock
        is not None.
        '''

        stocks = [Stock.get_or_none(ticker=stock_ticker) for stock_ticker in stock_tickers if Stock.get_or_none(ticker=stock_ticker) is not None]

        target_stocks = [stock.ticker for stock in stocks]

        if len(stocks) > 0:

            target_stocks_title = ', '.join(target_stocks)

            self.logger.info('Generating histogram for ' + target_stocks_title)

            scores = []

            for stock in stocks:

                stock_scores = [article_score.score for article_score in ArticleScore.select().join(Article, JOIN.INNER).join(StockArticle, JOIN.INNER).where((StockArticle.stock_ticker == stock) & (Article.save_date == date.today().__str__()))]

                scores.append(stock_scores)

            plt.hist(scores, bins=10, range=(-1,1), label=target_stocks)

            # This is the size of the "key".
            plt.legend(prop={'size' : 10})

            plt.suptitle(target_stocks_title)

            plt.show()    