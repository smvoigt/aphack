from ripe.atlas.sagan import Result

file = open("../resources/test2.json", "r")
data=file.readlines()
file.close

print(data)

my_result = Result.get([data])

my_result.af
# Returns 6

my_result.rtt_median
# Returns 123.456