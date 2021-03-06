from django.db import models

LEAGUE_CHOICES = (
    ('b', 'Bronze'),
    ('s', 'Silver'),
    ('g', 'Gold'),
    ('p', 'Platinum'),
    ('d', 'Diamond')
)

RACE_CHOICES = (
    ('t', 'Terran'),
    ('p', 'Protoss'),
    ('z', 'Zerg'),
    ('r', 'Random')
)

class Player(models.Model):
    name            = models.CharField(max_length=30, unique=True, verbose_name='Screen Name')
    league          = models.CharField(max_length=1, choices=LEAGUE_CHOICES)
    race            = models.CharField(max_length=1, choices=RACE_CHOICES)
    charcode        = models.IntegerField(verbose_name='Character Code')
    bnet_id         = models.IntegerField(unique=True, verbose_name = 'Battle.net ID #')
    portrait_id     = models.IntegerField()
    portrait_row    = models.IntegerField()
    portrait_col    = models.IntegerField()

    def sc2ranks_profile_url(self):
        return "http://sc2ranks.com/char/us/%s/%s" % (
            self.bnet_id, self.name
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

