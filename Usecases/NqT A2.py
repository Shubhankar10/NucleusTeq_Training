import pandas as pd
gods_df = pd.read_csv('greek_gods.csv')
goddesses_df = pd.read_csv('greek_goddesses.csv')

# 1.Merge the data from greek_gods.csv and greek_goddesses.csv based on a common field and create a new table that
# includes information about both gods and goddesses.

merged_df = pd.merge(gods_df, goddesses_df, how='outer', on='Domain',suffixes=('_god', '_goddess'))

print("Q1 : Merged DF :\n", merged_df.to_string())

# 2.Filter the merged table to only include gods and goddesses who are older than 8000 years, then sort them based on
# their ages in descending order.

filter_df = merged_df[(merged_df['Age_god'] > 8000) | (merged_df['Age_goddess'] > 8000)]
sorted_df = filter_df.sort_values(by=['Age_god', 'Age_goddess'], ascending=False)

print("\nQ2 : Sorted DF :\n", sorted_df)

# 3.Join the two tables based on the "Domain" field and calculate the average age of gods and goddesses in each domain

average_age = merged_df.groupby('Domain')[['Age_god', 'Age_goddess']].mean()
average_age.columns = ['Average Age of Gods', 'Average Age of Goddesses']

print("\nQ3 : Avg Age by Domain :\n", average_age)

# 4.Determine which god/goddess has the highest age, and then find out if they are a god or a goddess.

max_age = merged_df[['Age_god', 'Age_goddess']].max().max()
if max_age == merged_df['Age_god'].max():
    god_or_goddess = 'God'
else:
    god_or_goddess = 'Goddess'

print(f"\nQ4 : Among God and Goddess, {god_or_goddess} is Older. {god_name['God']} \n Age : {max_age} years.")

# 5.Create a new column in each table called "Age_Group" and categorize the gods/goddesses into groups such as
# "Young" (age < 5000), "Middle-aged" (age between 5000 and 8000), and "Old" (age > 8000).

def categorize_age(age):
    if age < 5000:
        return 'Young'
    elif 5000 <= age <= 8000:
        return 'Middle-aged'
    else:
        return 'Old'

gods_df['Age_Group'] = gods_df['Age'].apply(categorize_age)
goddesses_df['Age_Group'] = goddesses_df['Age'].apply(categorize_age)

print(f"\nQ5 : Categorize on age : \n Gods: \n {gods_df} \n Goddess: \n {goddesses_df}")

# 6.Compare the average ages of gods and goddesses. Is there a significant age difference between them? If yes,
# which group tends to be older?

avg_age_gods = gods_df['Age'].mean()
avg_age_goddesses = goddesses_df['Age'].mean()

print("\nQ6 : Age Difference in Gods and Goddess :")
print("Average age of Gods:", avg_age_gods)
print("Average age of Goddesses:", avg_age_goddesses)

if avg_age_gods > avg_age_goddesses:
    print("Gods are older on average.")
elif avg_age_gods < avg_age_goddesses:
    print("Goddesses are older on average.")
else:
    print("There's no significant age difference between gods and goddesses.")
    print("Average age of Gods and Goddesses:", avg_age_gods)

# 7.Write a Python program using for loop to iterate over the "Age" column of the merged table (after merging the
# gods and goddesses tables) and print out the names of gods/goddesses who are older than 8000 years. Filter the

print("\nQ7 : Gods/Goddesses older than 8000 years :")
merge_by_age = pd.merge(gods_df, goddesses_df, how='outer', on='Age', suffixes=('_god', '_goddess'))

for index, row in merge_by_age.iterrows():
    if row['Age'] > 8000:
        print(row['God'] if row['Age'] in gods_df['Age'].values else row['Goddess'])

# 8.Write a Python program to find the oldest god/goddess from the merged table (after merging the gods and goddesses
# tables) by iterating through the "Age" column using a while loop. Print out the name of the oldest god/goddess and
# their age.

oldest_name = None
oldest_age = -1
for index, row in merge_by_age.iterrows():
    if row['Age'] > oldest_age:
        oldest_age = row['Age']
        oldest_name = row['God'] if row['Age'] in gods_df['Age'].values else row['Goddess']
print(f"\nQ8 : Oldest Using Loop : \n The oldest god/goddess is {oldest_name} with an age of {oldest_age}.")
