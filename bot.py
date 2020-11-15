import discord
import newcovidpredictor

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    end, tomorrow, new_tot, diff, pending, hospital, total = newcovidpredictor.predictor()

    if message.content.startswith('$covidpred'):
        embed = discord.Embed(title='COVID Predictor',
                              description='Hello. Thank you for running the COVID-19 Predictor. \n\n'
                                   'We predict there will be ' + str(tomorrow) + ' new cases tomorrow and ' + str(new_tot) + ' '
                                    'total cases tomorrow. \n\n'
                                    'Today there are ' + str(pending) + ' pending cases yet to be deemed positive/negative. \n\n'
                                    'There are currently ' + str(hospital) + ' hospitalized COVID-19 patients. \n\n'
                                    'There were ' + str(total) + ' total cases today. \n\n'
                                    'We predict that COVID-19 will end ' + str(end) + ' days from April 1st 2020. \n\n'
                                    'Thank you come back tomorrow for a new prediction.')
        await message.channel.send(embed=embed)

client.run('Your Token Here')
