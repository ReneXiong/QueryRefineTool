## Name
QueryRefineTool

## Synopsis
QueryRefineTool [DBAddress] [DBPort] [Username] [Password] [DBName]

## Summary
QueryRefineTool is a python based tool for PostgreSQL query relaxation and contraction.
QueryRefineTool will provide range suggestions for tuples in the given desired range.

## Description
An example way to start the refine process: 
```commandline
> QueryRefineTool 127.0.0.1 5432 admin 123456 testBankDB
```

If the address is not reachable, QueryRefineTool will quit with a message of failed reason.
 
```commandline
"someRandomAddress:5432" is not reachable. 
```

After successful connection, 
QueryRefineTool will list every attribute with INTEGER type,
and ask user to choose which tuples they want to include in this refinement.

```commandline
"exampleBankTable" contains these INTEGER attributes:
1. AccountNo, 2. Age, 3. Balance, 4. CreditScore
Please select attributes you want to include, divided by comma. 

> 2,3,4

You choosed 2. Age, 3. Balance, 4. CreditScore
```

QueryRefineTool will ask for the desired amount of record. 

```commandline
Please enter the desired amount of record for your query
> 20
OK.
```

With the given amount, QueryRefineTool will list the possible range for every attribute.
This range is determined then you only individual attribute. 
If there aren't enough tuples at the beginning, QueryRefineTool will quit with a message of "No sufficient tuple".

```commandline
Current possible range (10000 est. possible tuples): 
1. Age, 2. Balance, 3. CreditScore
19-80   1-1000000   450-750
```

Then you can select the range of any attribute you want to set. 

```commandline
Current possible range (10000 est. possible tuples): 
1. Age, 2. Balance, 3. CreditScore
19-80   1-1000000   450-750

Please select the attribute you want to change  
> 1

Please enter the new range you want to set, format: min, max
> 10-18

Fail: No sufficient tuples. Please try again: 
Please select the attribute you want to change  
> 1

Please enter the new range you want to set, format: min, max
> 25-45

Current possible range (30 est. possible tuples): 
1. Age*, 2. Balance, 3. CreditScore
25-45   500-912345   450-750
Please select the attribute you want to change  
> 
```

You can set the second (and more) tuples:

```commandline
Current possible range (7000 est. possible tuples): 
1. Age*, 2. Balance, 3. CreditScore
25-45   500-912345   450-750
Please select the attribute you want to change   
> 3

Please enter the new range you want to set, format: min, max
> 700,750

Current possible range (100 est. possible tuples): 
1. Age*, 2. Balance, 3. CreditScore*
25-45   200000-1000000   700-750
Please select the attribute you want to change  
> 
```

If you set two (or more) ranges and there are no sufficient tuples, QueryRefineTool will try to loose other tuples you selected.
(In this example, the relaxed attribute is Age)
```commandline
Current possible range (100 est. possible tuples): 
1. Age*, 2. Balance, 3. CreditScore*
25-45   200000-1000000   700-750
Please select the attribute you want to change  
> 2

Please enter the new range you want to set, format: min, max
> 710000,750000

Current possible range (25 est. possible tuples): 
1. Age, 2. Balance*, 3. CreditScore*
20-55   710000,750000   700-750
Please select the attribute you want to change  
> 
```

## Note

Range of an unset attribute means, when only considering attribute that already set, this attribute has this range.
The method of selecting attributes to relax: it will try to relax only one attribute, by the sequence of attribute Number.
