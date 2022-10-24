from typing import List

# absChar = lambda a, b: abs(ord(a) - ord(b))
def absChar(a: str, b: str) -> int:
    return abs(ord(a) - ord(b))


# config
MAX_BOOKING = 20
MAX_TAXI = 4
START_POINT = "a"
END_POINT = "f"

MAX_DIST = absChar(START_POINT, END_POINT) + 1


class Taxi:
    def __init__(self):
        self.currentPosition = "a"
        self.earning = 0
        self.departureTime = 0

    def isTaxiFree(self, pickupTime) -> bool:
        return not self.departureTime >= pickupTime

    def setDepartureTime(self, pickUpPoint, dropPoint, pickUpTime) -> None:
        self.currentPosition = dropPoint
        self.departureTime = pickUpTime + absChar(pickUpPoint, dropPoint)


class Booking:
    def __init__(
        self,
        customer_id: int = 0,
        pickUpPoint: str = "a",
        dropPoint: str = "a",
        pickUpTime: int = 1,
    ) -> None:
        self.customer_id = customer_id
        self.pickUpTime = pickUpTime
        self.pickUpPoint = pickUpPoint
        self.dropPoint = dropPoint
        self.dropTime = 0
        self.taxiNo = 0
        self.earning = 0

    def getDropTime(self) -> None:
        self.dropTime = self.pickUpTime + absChar(self.pickUpPoint, self.dropPoint)

    def checkAvailability(self, taxiList: List[Taxi], taxiCount: int) -> int:
        taxiId = 0
        taxiid = 0
        shortestDistance = MAX_DIST
        while taxiId < taxiCount:
            dist = absChar(taxiList[taxiId].currentPosition, self.pickUpPoint)
            if taxiList[taxiId].isTaxiFree(self.pickUpTime):
                if dist < shortestDistance:
                    taxiid = taxiId
                elif (
                    dist == shortestDistance
                    and taxiList[taxiId].earning < taxiList[taxiid].earning
                ):
                    taxiid = taxiId

            shortestDistance = absChar(
                taxiList[taxiid].currentPosition, self.pickUpPoint
            )
            taxiId += 1
        if shortestDistance != MAX_DIST:
            taxiList[taxiid].setDepartureTime(
                self.pickUpPoint, self.dropPoint, self.pickUpTime
            )
            self.taxiNo = taxiid
            return taxiid

        return -1


class Main:
    def __init__(self):
        self.points = self.getListOfChar(START_POINT, END_POINT)
        self.bookingList: List[Booking] = self.initBooking()
        self.taxiList: List[Taxi] = self.initTaxi()
        self.bookingId: int = 0
        self.taxiId: int = MAX_TAXI
        self.main()

    def initBooking(self) -> List[Booking]:
        return [Booking() for i in range(MAX_BOOKING)]

    def initTaxi(self) -> List[Taxi]:
        return [Taxi() for i in range(MAX_TAXI + 1)]

    def getListOfChar(self, start: str, end: str) -> List[str]:
        return list(map(chr, range(ord(start), ord(end) + 1)))

    def getNumber(self, msg: str = "") -> int:
        while True:
            num = input(msg)
            if num.isnumeric():
                return int(num)
            print("Pls Enter Number..!")

    def getPoint(self, msg: str = "") -> str:
        while True:
            point = input(msg)
            if point in self.points:
                return str(point)
            print("Pls Enter Point Between {} to {}..!".format(START_POINT, END_POINT))

    def printTable(self, header: List[str], rows: List[List[str]]) -> str:
        row = " {} |" * (len(header))
        border = ""
        row_format = ""

        for head in header:
            headlen = len(head)
            border += "+" + ("-" * (headlen + 2))
            row_format += "| {:>" + str(headlen) + "} "

        row_format += "|"
        border += "+"
        row = "\n|" + row
        table = border + row.format(*header) + "\n" + border + "\n"
        for row in rows:
            table += row_format.format(*row) + "\n"

        table += border
        print(table)
        return table

    def getPrice(self, pickUpPoint: str, dropPoint: str) -> int:
        return (((absChar(pickUpPoint, dropPoint) * 15) - 5) * 10) + 100

    def bookingDetails(self) -> None:
        header = [
            "BookingId",
            "CustomerId",
            "TaxiNo",
            "PickupPoint",
            "DropPoint",
            "PickupTime",
            "DropTime",
            "Earnings",
        ]
        bookingid = 0
        data = []
        while bookingid < self.bookingId:
            row = [
                bookingid,
                self.bookingList[bookingid].customer_id,
                self.bookingList[bookingid].taxiNo,
                self.bookingList[bookingid].pickUpPoint,
                self.bookingList[bookingid].dropPoint,
                self.bookingList[bookingid].pickUpTime,
                self.bookingList[bookingid].dropTime,
                self.bookingList[bookingid].earning,
            ]
            data.append(row)
            bookingid += 1
        self.printTable(header=header, rows=data)

    def taxiDatils(self) -> None:
        id = 0
        rows = []
        header = ["Taxi No", "Current Position", "Total Earning"]
        while id < self.taxiId:
            taxi = self.taxiList[id]
            rows.append([id, taxi.currentPosition.upper(), taxi.earning])
            id += 1
        self.printTable(header, rows)

    def booking(self) -> None:
        customer_id = self.getNumber("Customer Id :")
        pickup_point = self.getPoint("Pickup Point :")
        drop_point = self.getPoint("Drop Point :")
        pickup_time = self.getNumber("Pickup Time :")

        self.bookingList[self.bookingId] = Booking(
            customer_id, pickup_point, drop_point, pickup_time
        )
        availableTaxi = self.bookingList[self.bookingId].checkAvailability(
            self.taxiList, self.taxiId
        )
        if availableTaxi != -1:
            print("Your booking is successfull with taxi no: {}".format(availableTaxi))
            self.bookingList[self.bookingId].getDropTime()
            self.calcEarnings(self.bookingId, availableTaxi)
            self.bookingId += 1
        else:
            print("No taxi is free for your pickUpTime!!")
            print("You may chance your pickup time and try your booking!!")

    def calcEarnings(self, bookingId: int, taxiId: int) -> None:
        pickUpPoint = self.bookingList[bookingId].pickUpPoint
        dropPoint = self.bookingList[bookingId].dropPoint
        earning = self.getPrice(pickUpPoint, dropPoint)
        self.bookingList[bookingId].earning = earning
        self.taxiList[taxiId].earning += earning

    def main(self) -> None:
        while True:
            print(
                "__________Call_Taxi_Booking___________"
                + "\n1.Booking"
                + "\n2.Booking Details"
                + "\n3.Taxi Details"
                + "\n4.Exit"
                + "\nEnter ur choice:"
            )
            choice = self.getNumber("Enter Choice:")
            if choice == 4:
                print("Thank U... :)")
                break
            elif choice == 3:
                self.taxiDatils()
            elif choice == 2:
                self.bookingDetails()
            elif choice == 1:
                self.booking()


if __name__ == "__main__":
    Main()
