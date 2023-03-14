# A class to store a Job
class Job:
    def __init__(self, start, finish, profit):
        self.start = start
        self.finish = finish
        self.profit = profit


# Function to find the index of the last job which doesn't conflict with the given job.
# It performs a linear search on the given list of jobs.
def findLastNonConflictingJob(jobs, n):
    # find the last job index whose finish time is less than or equal to the
    # given job's start time
    for i in reversed(range(n)):
        if jobs[i].finish <= jobs[n].start:
            return i

    # return the negative index if no non-conflicting job is found
    return -1


# A recursive function to find the maximum profit subset of non-overlapping
# jobs, which are sorted according to finish time
def findMaxProfitBF(jobs, n):
    # base case
    if n < 0:
        return 0

    # return if only one item is remaining
    if n == 0:
        return jobs[0].profit

    # find the index of the last non-conflicting job with the current job
    index = findLastNonConflictingJob(jobs, n)

    # include the current job and recur for non-conflicting jobs `[0, index]`
    incl = jobs[n].profit + findMaxProfitBF(jobs, index)

    # exclude the current job and recur for remaining items `[0, n-1]`
    excl = findMaxProfitBF(jobs, n - 1)

    # return the maximum profit by including or excluding the current job
    return max(incl, excl)


# Wrapper over `findMaxProfit()` function
def maxProfit(jobs):
    import time

    # sort jobs in increasing order of their finish times
    jobs.sort(key=lambda x: x.finish)

    # get time for DP
    tic = time.perf_counter()
    findMaxProfitDP(jobs)
    toc = time.perf_counter()
    timer = toc - tic
    timer = "{:.8f}".format(timer)
    print("The time elapsed in the DP algorithm is " + str.format(timer) + ".")

    # get time for DP recursive
    tic = time.perf_counter()
    maxProfitDPRecWrap(jobs)
    toc = time.perf_counter()
    timer = toc - tic
    timer = "{:.8f}".format(timer)
    print("The time elapsed in the recursive DP algorithm is " + str.format(timer) + ".")

    # get time for BF
    tic = time.perf_counter()
    findMaxProfitBF(jobs, len(jobs) - 1)
    toc = time.perf_counter()
    timer = toc - tic
    timer = "{:.8f}".format(timer)
    print("The time elapsed in the BF algorithm is " + str.format(timer) + ".")

    findMaxProfitJobs(jobs)
    print(" -> total profit:  ",  end=' ')
    print(findMaxProfitBF(jobs, len(jobs) - 1))


# Function to find the maximum profit of non-overlapping jobs using DP
def findMaxProfitDP(jobs):
    # base case
    if not jobs:
        return 0

    # sort jobs in increasing order of their finish times
    jobs.sort(key=lambda x: x.finish)

    # construct a lookup table where the i'th index stores the maximum profit
    # for the first `i` jobs
    maxProfit = [None] * len(jobs)

    # maximum profit gained by including the first job
    maxProfit[0] = jobs[0].profit

    # fill the `maxProfit` table in a bottom-up manner from the second index
    for i in range(1, len(jobs)):

        # find the index of the last non-conflicting job with the current job
        index = findLastNonConflictingJob(jobs, i)

        # include the current job with its non-conflicting jobs
        incl = jobs[i].profit
        if index != -1:
            incl += maxProfit[index]

        # store the maximum profit by including or excluding the current job
        maxProfit[i] = max(incl, maxProfit[i - 1])

    # return maximum profit
    return maxProfit[-1]


# Function to perform a binary search on the given jobs, which are sorted
# by finish time. The function returns the index of the last job, which
# doesn't conflict with the given job, i.e., whose finish time is
# less than or equal to the given job's start time.
def findLastNonConflictingJob(jobs, n):
    # search space
    (low, high) = (0, n)

    # iterate till the search space is exhausted
    while low <= high:
        mid = (low + high) // 2
        if jobs[mid].finish <= jobs[n].start:
            if jobs[mid + 1].finish <= jobs[n].start:
                low = mid + 1
            else:
                return mid
        else:
            high = mid - 1

    # return the negative index if no non-conflicting job is found
    return -1


# Function to print the non-overlapping jobs involved in maximum profit
# using dynamic programming
def findMaxProfitJobs(jobs):
    # base case
    if not jobs:
        return 0

    # sort jobs in increasing order of their finish times
    jobs.sort(key=lambda x: x.finish)

    # get the number of jobs
    n = len(jobs)

    # `maxProfit[i]` stores the maximum profit possible for the first `i` jobs, and
    # `tasks[i]` stores the index of jobs involved in the maximum profit
    maxProfit = [None] * n
    tasks = [[] for _ in range(n)]

    # initialize `maxProfit[0]` and `tasks[0]` with the first job
    maxProfit[0] = jobs[0].profit
    tasks[0].append(0)

    # fill `tasks[]` and `maxProfit[]` in a bottom-up manner
    for i in range(1, n):

        # find the index of the last non-conflicting job with the current job
        index = findLastNonConflictingJob(jobs, i)

        # include the current job with its non-conflicting jobs
        currentProfit = jobs[i].profit
        if index != -1:
            currentProfit += maxProfit[index]

        # if including the current job leads to the maximum profit so far
        if maxProfit[i - 1] < currentProfit:
            maxProfit[i] = currentProfit

            if index != -1:
                tasks[i] = tasks[index][:]
            tasks[i].append(i)

        # excluding the current job leads to the maximum profit so far
        else:
            tasks[i] = tasks[i - 1][:]
            maxProfit[i] = maxProfit[i - 1]

    # `tasks[n-1]` stores the index of jobs involved in the maximum profit
    print("The jobs involved in the maximum profit are", end=' ')
    for i in tasks[n - 1]:
        print((jobs[i].start, jobs[i].finish, jobs[i].profit), end=' ')


# A recursive function to find the maximum profit subset of non-overlapping
# jobs, which are sorted according to finish time
def findMaxProfitDPRec(jobs, n):

    # base case
    if n < 0:
        return 0

    # return if only one item is remaining
    if n == 0:
        return jobs[0].profit

    # find the index of the last non-conflicting job with the current job
    index = findLastNonConflictingJob(jobs, n)

    # include the current job and recur for non-conflicting jobs `[0, index]`
    incl = jobs[n].profit + findMaxProfitDPRec(jobs, index)

    # exclude the current job and recur for remaining items `[0, n-1]`
    excl = findMaxProfitDPRec(jobs, n - 1)

    # return the maximum profit by including or excluding the current job
    return max(incl, excl)


# Wrapper over `findMaxProfit()` function
def maxProfitDPRecWrap(jobs):

    # sort jobs in increasing order of their finish times
    jobs.sort(key=lambda x: x.finish)

    return findMaxProfitDPRec(jobs, len(jobs) - 1);


def allJobs(jobs):
    # base case
    if not jobs:
        return 0
    # sort jobs in increasing order of their finish times
    jobs.sort(key=lambda x: x.finish)

    # get the number of jobs
    n = len(jobs)

    for i in range(1, n):
        print("option " + str(i) + ": ",  end=' ')
        prof = jobs[i].profit
        for p in range(i, n):
            if jobs[i].finish <= jobs[p].start:
                print((jobs[p].start, jobs[p].finish, jobs[p].profit), end=' ')
                prof += jobs[p].profit
        print("-> total profit: ", end=" ")
        print(prof)


if __name__ == '__main__':

    numJobs = int(input("Enter number of jobs: "))

    jobs = [None]*numJobs

    for i in range(0, numJobs):
        print("Job ", end=" ")
        print(i + 1, end=" ")
        start = int(input(" enter start time: "))
        print("Job ", end=" ")
        print(i + 1, end=" ")
        finish = int(input(" enter end time: "))
        print("Job ", end=" ")
        print(i + 1, end=" ")
        profit = int(input(" enter profit of job: "))
        jobs[i] = Job(start, finish, profit)

    maxProfit(jobs)

    allJobs(jobs)
