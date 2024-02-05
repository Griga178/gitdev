from sqlalchemy import desc

def get_last_conrtact_date(self):
    '''
    Получение даты последнего отпарсенного контракта
    '''
    try:
        with self.app.app_context():
            a = self.Contrant_card.query.order_by(desc(self.Contrant_card.date)).first()

        return a.date
    except:
        # print('None')
        return None
