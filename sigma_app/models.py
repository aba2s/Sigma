"""
Models in Django are equivalents to tables in SQL. A model is the single,
definitive source of information about data. It contains the essential
fields and behaviors of the data we're storing. Generally, each model
maps to a single database table.

The basis:

* Each model is a Python class that subclasses **django.db.models.Model**.
* Each attribute of the model represents a database field.
* With all of this Django gives you an automatically-generated
  database-access PAI.

**Quick example:**
This example model defines a **Person**, which hase a **first_name**
and **last_name**.

::

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)


All model relationship create dependencies between one another, so an important
behavior is
what happens to the other party when one party is removed. The on_delete option
is designed
for this purpose, to determine what to do with records on the other side of a
relationship
when one side is removed. The on_delete option is available for all three
relationship model
data types. Here is an exellent book about this topic
https://www.webforefront.com/django/setuprelationshipsdjangomodels.html

"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# How to Create a Date Form Field in a Django form
# birth_date= forms.DateField(label='What is your birth date?',
# widget=forms.SelectDateWidget)

alphanumeric = RegexValidator(
    regex=r'^[a-zA-Z -]+$',
    message='Only alphanumeric characters are allowed.',
    code='Invalid advertiser name')

def validate_name(value):
    if len(value) < 3:
        raise ValidationError(
            '{} is too sort for an advertiser name'.format(value)
        )

"""Incoming camapaigns table"""

class IncomingCampaigns(models.Model):
    """Managers or consultants can attribute campaigns to users

    start_date, end_date, name, KPI, advertiser, user(am, consultant),
    description etc
    with IO file containing the signed budget.
    Push notification de la part du consultant à ou vers l'account qui
    gere la campagne.
    """
    pass


"""
Campaign Naming Tool table
--------------------------
"""
class CampaignNamingTool(models.Model):
    """
    The goal of Campaign Naming Tool is to help account mangers
    to plan their campaigns and to follow nomenclature guidelines
    and thus avoid bugs or missing campaigns. Because campaigns
    are case sensitives in the workflow process. So every bad
    named or misnamed campaign are ignored and it won't be
    displayed in the users insertions orders. Plase use this
    formular to create your campaign for the first time.

    .. admonition:: Important

       If the campaign does not respect the guidelines, you
       can't follow it here. It will be missing in the monitoring.

    Parameters
    ----------
    user                          : owner or in charge of the campaign.
    year, month                   : year and month when launching
                                    campaign online.
    advertiser                    : advertiser of the campaign.
    name                          : name of the campaign.
    device                        : device the campaign must be served
                                    (Desktop, Mobile, tablette).
    type_of_format                : format that campaign must be served
                                    (IAB, Video, etc)
    kpi                           : KPI of the campaign (CPM, CPC, CPV,
                                    CPA, etc)

    Returns
    -------
    an Insertion Order object composed by the concatenation of all
    these parameters
    """

    year_choices = (
        ('2021', '2021'), ('2022', '2022'), ('2023', '2023'),
        ('2024', '2024'), ('2025', '2025'), ('2026', '2026'),
        ('2027', '2027'), ('2028', '2028'), ('2029', '2029'),
        ('2030', '2030'), ('2031', '2031'),
    )

    month_choices = (
        ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
        ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
        ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'),
    )

    kpi_choices = (
        ('CPA', 'CPA'), ('CPC', 'CPC'), ('CPD', 'CPD'),
        ('CPL', 'CPL'), ('CPM', 'CPM'), ('CPV', 'CPV'),
        ('CTR', 'CTR'), ('Vsibility', 'Visibility'),
        ('VTR', 'VTR'), ('LTR', 'LTR'),
    )

    format_choices = (
        ('Audio', 'Audio'), ('Facebook', 'Facebook'),
        ('Habi.', 'Habi.'), ('Habi. slid.', 'Habi. slid.'),
        ('Habi. swap', 'Habi. swap'), ('Habi. vid.', 'Habi. vid.'),
        ('IAB', 'IAB'), ('Impact.', 'Impact.'), ('Interst.', 'Interst.'),
        ('Interst. video', 'Interst. video'), ('Native', 'Native'),
        ('Parallax', 'Parallax'), ('Vid. pre-roll', 'Vid. pre-roll'),
        ('Vid. in-read', 'Vid. in-read'),
        ('Vid. in-banner', 'Vid. in-banner'),
        ('Vid. in-banner', ' Social + IAB'), ('Vid. in-banner', 'Social'),
    )

    device_choices = (
        ('Multi-device', 'Multi-device'), ('PC', 'PC'), ('Mob.', 'Mob.'),
        ('Tab.', 'Tab.'), ('Mob. + tab.', 'Mob. + tab.'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, choices=year_choices)
    month = models.CharField(max_length=4, choices=month_choices)
    advertiser = models.CharField(max_length=80, validators=[alphanumeric])
    name = models.CharField(max_length=100, validators=[validate_name])
    device = models.CharField(max_length=30, choices=device_choices,
        default='Multi-device')
    type_of_format = models.CharField(max_length=30,
        choices=format_choices, default='IAB')
    kpi = models.CharField(max_length=10, choices=kpi_choices, default='CPM')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String for representing the Model object."""
        return "{}-{} - {} - {} - {} - {} - {}".format(
            self.year.strip(), self.month.strip(),
            self.advertiser.strip(), self.name.strip(),
            self.device.strip(), self.type_of_format.strip(),
            self.kpi.strip())

    class Meta:
        db_table = 'CampaignNamingTool'
        unique_together = ['year', 'month', 'advertiser',
                           'name', 'kpi', 'type_of_format',
                           'device']


"""
User Insertion Orders table
---------------------------
"""
class UserInsertionOrder(models.Model):
    """
    This table contains only the insertion order of logged user.
    The one who created the insertions order. Doing thus, user
    can only see her/his campaigns. So logged user doesn't have
    access to others users's campaigns. It make the UI more fluide
    compared to other tools like Datorama.

    Parameters
    ----------
    user                          : owner or in charge of the campaign.
    campaign_naming_tool          : the insertion order object we created
                                    with CNT
    budget                        : the signed budget for the entire
                                    duration of the campaign.
    kpi                           : KPI of the campaign (CPM, CPC, CPV,
                                    CPA, etc)
    goal_value                    : goal of the campaign to reach.
    start_date                    : campaign start day.
    end_date                      : campaign end day.

    Returns
    -------
    an Insertion Order object.
    """
    kpi_choices = (
        ('CPA', 'CPA'), ('CPC', 'CPC'),
        ('CPD', 'CPD'), ('CPL', 'CPL'),
        ('CPM', 'CPM'), ('CPV', 'CPV'),
        ('CTR', 'CTR'), ('Vsibility', 'Visibility'),
        ('VTR', 'VTR'), ('LTR', 'LTR'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_naming_tool = models.ForeignKey(
        CampaignNamingTool, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    kpi = models.CharField(max_length=10, choices=kpi_choices)
    goal_value = models.DecimalField(max_digits=20, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "%s" % self.campaign_naming_tool
        # return "{} - [{}]".format(self.insertion_order, self.user)

    class Meta:
        db_table = 'UserInsertionOrder'
        unique_together = ['campaign_naming_tool']


"""
User Insertion Orders By DSP table
----------------------------------
"""
class UserInsertionOrderByDSP(models.Model):
    """
    Here we split the signed budget filled in **User Insertion Orders table**
    between DSP or partners. At the end campaing the whole budget must be
    equal to the signed budget.

    Parameters
    ----------
    user                          : owner or in charge of the campaign.
    insertion_order               : the insertion order object we created.
    dsp                           : the Demand Side Platform or the partner.
    budget                        : the budget we want to put in this **DSP**.
    start_date                    : campaign start day.
    end_date                      : campaign end day.

    Returns
    -------
    an Insertion Order object.
    """
    dsp_choices = (
        ('Amazon', 'Amazon'),
        ('Amobee', 'Amobee'),
        ('AppNexus', 'AppNexus'),
        ('Digiteka', 'Digiteka'),
        ('DV 360', 'DV 360'),
        ('Oath', 'Oath')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insertion_order = models.ForeignKey(UserInsertionOrder,
                                        on_delete=models.CASCADE)
    dsp = models.CharField(max_length=30, choices=dsp_choices)
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    # optionel, on prend par defaut celui de InsertionOrder
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{} - [{}]".format(self.insertion_order, self.dsp)

    class Meta:
        db_table = 'UserInsertionOrderByDSP'
        unique_together = ['insertion_order', 'dsp']


class InsertionOrdersCommonFields(models.Model):
    date = models.DateField('Date')
    advertiser = models.CharField('Advertiser', max_length=100)
    insertion_order = models.ForeignKey(UserInsertionOrder,
        on_delete=models.CASCADE)
    dsp = models.CharField(max_length=20)
    strategy = models.CharField('Strategy Name', max_length=300)
    creative = models.CharField('Creative Name', max_length=400)
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    impressions = models.PositiveBigIntegerField()
    clicks = models.PositiveBigIntegerField()
    conversions = models.IntegerField()
    post_clicks_conversions = models.IntegerField()
    post_views_conversions = models.IntegerField()

    def __str__(self):
        return "{} - [{}]".format(self.insertion_order, self.dsp)


    class Meta:
        abstract = True # this tells Django, not to create
        # a database table for the corresponding models.


class DV360(InsertionOrdersCommonFields):
    dsp = models.CharField('DV360', max_length=20)
    
    class Meta:
        db_table = 'DV360'
        # verbose_name_plural = "companies" his simply makes
        # sure that in our admin panel the class is called companies
        # in the plural and not companys

class Xandr(InsertionOrdersCommonFields):
    dsp = models.CharField('Xandr', max_length=20)

    class Meta:
        db_table = 'Xandr'


class Dynamic(InsertionOrdersCommonFields):
    dsp = models.CharField('Dynamic', max_length=20)

    class Meta:
        db_table = 'Dynadmic'


class FreeWheel(InsertionOrdersCommonFields):
    dsp = models.CharField('FreeWheel', max_length=20)

    class Meta:
        db_table = 'FreeWheel'


"""
Datorama Insertion Orders table
-------------------------------
"""
class InsertionOrdersRealSpents(InsertionOrdersCommonFields):
    """
    This is a very important part. This table contains all user campaigns's
    data. The data content impressions, clicks, budget, etc. It's gived by
    day for the last week. It's the consolidated data of all DSP.

    .. admonition:: Note

      Only campaigns respecting **Camapign Naming Tool** guidelines will
      be displayed if they have been served impressions. IF the campaign does
      not serve, it wont be displayed here.

    Parameters
    ----------
    date                          : daily campaign's delivery
    dsp                           : the Demand Side Platform or the partner
    advertiser                    : advertiser of the campaign
    insertion_order               : lauched insertion order
    strategy                      : campaign's strategies (context,
                                    comportemental,socio-demo)
    creative                      : creative that campaign must be
                                    served (pave, megaban, etc)
    kpi                           : KPI of the campaign (CPM, CPC, CPV, CPA,
                                    etc)
    impressions                   : served impressions during that day
    clicks                        : clicks generated during that day
    conversions                   : conversions registred during that day
    post_clicks_conversions       : conversions generated after clicking
    post_views_conversions        : conversions generated after seeing
                                    an impression

    Returns
    -------
    many Insertion Orders with metrics.
    """

    def __str__(self):
        return "%s" % self.insertion_order
        # return "{}".format(self.insertion_order)

    class Meta:
        db_table = 'InserstionOrdersRealSpents'''


class AsynchroneTask(models.Model):
    INPROGRESS = 0
    FINISHED = 1
    FAILED = 2
    STATUS_CHOICES = (
        (INPROGRESS, 'In-progress'),
        (FINISHED, 'Finished'),
        (FAILED, 'Failed'),
    )
    id = models.UUIDField(primary_key=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField(null=True)
    status = models.SmallIntegerField(default=0, choices=STATUS_CHOICES)
    status_result = models.TextField(null=True, blank=True)
    dv360 = models.ForeignKey(DV360, on_delete=models.CASCADE, null=True)
    xandr = models.ForeignKey(Xandr, on_delete=models.CASCADE, null=True)
    dynamic = models.ForeignKey(Dynamic, on_delete=models.CASCADE, null=True)
    freewheel = models.ForeignKey(FreeWheel, on_delete=models.CASCADE, null=True)
    
    def get_status(self):
        return self.STATUS_CHOICES[self.status][1]
    
    def __str__(self):
        if self.dv360:
            return "{} - ".format(self.dv360, self.status)
        
        elif self.xandr:
            return "{} - {}".format(self.xandr, self.status)
        elif self.dynamic:
            return "{} - {}".format(self.dynamic, self.status)
        elif self.freewheel:
            return "{} - {}".format(self.freewheel, self.status)
        else:
            return "Inconnu - {}".format(self.status)


    class Meta:
        db_table = 'AsynchroneTask'


class BatchName(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dsp = models.CharField(max_length=50)
    status = models.ForeignKey(AsynchroneTask, on_delete=models.CASCADE)
    total_rows = models.PositiveIntegerField()
    valid_rows = models.PositiveIntegerField()
    invalid_rows = models.PositiveBigIntegerField()
    file_name = models.CharField(max_length=300)

    def __str__(self):
        return "{} - {}".format(self.dsp, self.file_name)
    
    class Meta:
        db_table = 'BatchName'


'''class Manager(User):
    """Managers have to add users under their management to their account.
    Doing this allows them to have access of these users's campaigns
    """
    def __init__(self, account_managers=None, *args, **kwargs):
        super()._init(*args, **kwargs)
        if account_managers is None:
            self.account_managers = []
        else:
            self.account_managers = account_managers

    def add_account_manager(self, am):
        if am not in self.account_managers:
            self.account_managers.append(am)

    def remove_account_manager(self, am):
        if am in self.account_managers:
            self.account_managers.remove(am)'''

