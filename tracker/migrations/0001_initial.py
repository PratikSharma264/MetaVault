from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Profile', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(default='Alex',max_length=80)),('daily_calorie_goal',models.PositiveIntegerField(default=2200)),('daily_protein_goal',models.PositiveIntegerField(default=150)),('daily_water_goal',models.PositiveIntegerField(default=8)),('streak',models.PositiveIntegerField(default=12))]),
        migrations.CreateModel(name='FoodEntry', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=120)),('meal',models.CharField(choices=[('breakfast','Breakfast'),('lunch','Lunch'),('dinner','Dinner'),('snack','Snack')],max_length=12)),('calories',models.PositiveIntegerField()),('protein',models.DecimalField(decimal_places=1,default=0,max_digits=6)),('carbs',models.DecimalField(decimal_places=1,default=0,max_digits=6)),('fat',models.DecimalField(decimal_places=1,default=0,max_digits=6)),('eaten_at',models.DateField(auto_now_add=True)),('created_at',models.DateTimeField(auto_now_add=True))],options={'ordering':['-created_at']}),
        migrations.CreateModel(name='WaterEntry', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('amount_ml',models.PositiveIntegerField(default=250)),('consumed_at',models.DateField(auto_now_add=True))]),
        migrations.CreateModel(name='Workout', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=120)),('duration_minutes',models.PositiveIntegerField()),('calories_burned',models.PositiveIntegerField(default=0)),('completed_at',models.DateField(auto_now_add=True))])]
