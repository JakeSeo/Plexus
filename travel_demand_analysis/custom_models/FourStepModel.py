import pandas as pd

class TripGeneration:
    def __init__(self, pathToData, dependent_col_name):
        self.pathToData = pathToData
        self.dependent_col_name = dependent_col_name
        self.production_col_names = []
        self.production_constant = 0
        self.production_intercepts = []
        self.attraction_col_names = []
        self.attraction_constant = 0
        self.attraction_intercepts = []
        self.production_score = 0
        self.attraction_score = 0
        self.balancing_factor = 0

    def printAttributes(self):
        print("Attributes")
        print(self.production_col_names)
        print(self.production_constant)
        print(self.production_intercepts)
        print(self.attraction_col_names)
        print(self.attraction_constant)
        print(self.attraction_intercepts)

    def setProductionParameters(self, production_col_names, production_constant, production_intercepts):
        self.production_col_names = production_col_names
        self.production_constant = production_constant
        self.production_intercepts = production_intercepts

    def setAttractionParameters(self, attraction_col_names, attraction_constant, attraction_intercepts):
        self.attraction_col_names = attraction_col_names
        self.attraction_constant = attraction_constant
        self.attraction_intercepts = attraction_intercepts

    # get trip production score for 'zone'
    def getWholeTripProductionScore(self):
        data = pd.read_csv(self.pathToData, encoding="utf-8",index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        sub_table = data.loc[:, self.production_col_names]
        length_rows = sub_table.shape[0]
        for x in range(0, length_rows):
            row_values = sub_table.iloc[x, :].values
            self.production_score += self.production_constant
            print(str(row_values))
            for j in range(0, len(row_values)):
                print(str(self.production_col_names[j])+" ROW_VALUES: "+str(row_values[j]))
                self.production_score += int(row_values[j] * self.production_intercepts[j])
                # print("SELFPROD CURR: "+str(self.production_score))
        return int(self.production_score)

    # get trip attraction score for 'zone'
    def getWholeTripAttractionScore(self):
        data = pd.read_csv(self.pathToData, index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        sub_table = data.loc[:, self.attraction_col_names]
        length_rows = sub_table.shape[0]
        for x in range(0, length_rows):
            row_values = sub_table.iloc[x, :].values
            self.attraction_score += self.attraction_constant
            for j in range(0, len(row_values)):
                self.attraction_score += int(row_values[j] * self.attraction_intercepts[j])
                # print("SELFATTR CURR: "+str(self.attraction_score))
        return int(self.attraction_score)

    def getZoneTripProductionScore(self, zone_number):
        self.production_score = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        row_values = data.loc[zone_number, self.production_col_names].values

        self.production_score += self.production_constant
        for j in range(0, len(row_values)):
            self.production_score += row_values[j] * self.production_intercepts[j]

        return self.production_score

    def getZoneTripAttractionScore(self, zone_number):
        self.attraction_score = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        row_values = data.loc[zone_number, self.production_col_names].values

        self.attraction_score += self.attraction_constant
        for j in range(0, len(row_values)):
            self.attraction_score += row_values[j] * self.attraction_intercepts[j]

        return self.attraction_score

    def doTripBalancing(self):
        self.balancing_factor = self.production_score / self.attraction_score
        self.attraction_score = self.balancing_factor * self.attraction_score
        self.production_score = self.balancing_factor * self.production_score
        # Implement trip balancing here VOID

    def getBalancingFactor(self):
        return self.balancing_factor

    def printAllZonalTripsProductionAttraction(self):
        productionScores = []
        attractionScores = []
        df = pd.DataFrame(columns=('Trip Production', 'Trip Atraction'))
        total_production = 0
        total_attraction = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        length_rows = data.shape[0]
        for x in range(0, length_rows):
            attr_score = 0
            prod_score = 0
            #print("data_cols: "+str(data.columns.values))
            #print("attr_cols: "+str(self.attraction_col_names))
            attr_row_values = data.loc[x, self.attraction_col_names].values
            prod_row_values = data.loc[x, self.production_col_names].values
            attr_score += self.attraction_constant
            prod_score += self.production_constant
            for j in range(0, len(attr_row_values)):
                attr_score += attr_row_values[j] * self.attraction_intercepts[j]
            total_attraction += attr_score
            for j in range(0, len(prod_row_values)):
                prod_score += prod_row_values[j] * self.production_intercepts[j]
            total_production += prod_score
            df.loc[x] = [int(prod_score), int(attr_score)]
            productionScores.append(int(prod_score))
            attractionScores.append(int(attr_score))
            # print("Zone "+str(x)+": Production="+str(prod_score)+" , Attraction="+str(attr_score))
        return df, productionScores, attractionScores;
        # print("Total Production="+str(total_production)+" , Total Attraction="+str(total_attraction))

    def getTripProductionScores(self):
        productionScores = []
        total_production = 0
        total_attraction = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        length_rows = data.shape[0]
        for x in range(1, length_rows + 1):
            prod_score = 0
            prod_row_values = data.loc[x, self.production_col_names].values
            prod_score += self.production_constant
            for j in range(0, len(prod_row_values)):
                prod_score += prod_row_values[j] * self.production_intercepts[j]
            total_production += prod_score
            productionScores.append(prod_score)
        return productionScores

    def getProductionSubTable(self):
        data = pd.read_csv(self.pathToData, index_col=0)
        return data.loc[:, self.production_col_names]