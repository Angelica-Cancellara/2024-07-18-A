from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                    FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getCromosoma():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Chromosome 
                        from genes g 
                        order by Chromosome asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                       FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(cmin, cmax):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from genes g
                    where g.Chromosome >= %s and g.Chromosome <= %s"""
        cursor.execute(query, (cmin, cmax))
        for row in cursor:
            result.append(Gene(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(cmin, cmax, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select g1.GeneID as g1, g2.GeneID as g2, g1.Function as f1, g2.Function as f2, i.Expression_Corr as peso
                from classification c1, classification c2, genes g1, genes g2, interactions i 
                where c1.GeneId = g1.GeneID 
                and c2.GeneID = g2.GeneID 
                and c1.Localization = c2.Localization 
                and c1.GeneID != c2.GeneID
                and g1.Chromosome <= g2.Chromosome 
                and ((c1.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2) or (c1.GeneID = i.GeneID2 and c2.GeneID = i.GeneID1))
                and g1.Chromosome >= %s
                and g1.Chromosome <= %s
                and g2.Chromosome >= %s
                and g2.Chromosome <= %s"""
        cursor.execute(query, (cmin, cmax, cmin, cmax))
        for row in cursor:
            result.append((idMap[row["g1"], row["f1"]], idMap[row["g2"], row["f2"]], row["peso"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_localizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT c.Localization  
                            FROM classification c 
                            ORDER BY c.Localization  ASC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result