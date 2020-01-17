# Changing Weapons Settings
It should be noted that using this editor to adjust the settings of weapons may have unexpected results, specifically when adjusting the 'Power' values. 

Ammo
----
A value of 10 or any integer between 128 and 255, inclusive, will result in infinite ammo. Else, you will start with as much ammo as you input.

Delay
-----
A value between 128 and 255, inclusive, will result in an unlimited delay, which will also stop it from appearing in crates if it's a super weapon.

Crate probability
-----------------
I'm not entirely sure but my understanding is that the crate probabilities of all the weapons are proprtional to each other. For example, if every weapon had a crate probability of 1, they would all be equally likely to appear in crates. Further, you would get the exact same result if you set every probability to 2 (or 3, 4, etc.). If you set the Bazooka to probability 1, and the ninja ropes to 2, the ninja ropes should be twice as likely to appear in a crate as the bazooka.



Power
-------------------

The best way to decide what you want power-wise is to use the 'Weapon List' and 'Super Weapons' sections under https://worms2d.info/Game_scheme_file, clicking the links to go a weapon's page. This page should display a table describing exactly what each power value does to this weapon. I haven't personally tested what happens beyond the values they list, since many tables don't include all 256 possible power values.

Many super weapons don't seem to be affected by changes to power.

NOTE: You should subtract 1 one from the suggested power values listed on the website as they are off by 1.

**Looking at the bazooka as an example**

Table retrieved from https://worms2d.info/Bazooka:

<!-- If they're not indenting this, I'm not doing it for them -->
<table class="infobox" style="width: 15em; font-size: 90%;">
<tbody><tr>
<td>
<table width="100%">
<caption style="font-size: 100%;"> <span style="font-size: 150%; font-weight: bold;">Power settings</span>
</caption>
<tbody><tr>
<th> Power
</th>
<th> Maximum injury
</th>
<th> Crater diameter
</th></tr>
<tr>
<td>11
</td>
<td>25 hp
</td>
<td>47 px
</td></tr>
<tr>
<td>12
</td>
<td>35
</td>
<td>73
</td></tr>
<tr>
<td>1
</td>
<td>40
</td>
<td>85
</td></tr>
<tr>
<td>2
</td>
<td>45
</td>
<td>85
</td></tr>
<tr>
<td>3
</td>
<td>50
</td>
<td>97
</td></tr>
<tr>
<td>4
</td>
<td>55
</td>
<td>111
</td></tr>
<tr>
<td>5
</td>
<td>60
</td>
<td>123
</td></tr>
<tr>
<td>19
</td>
<td>65
</td>
<td>123
</td></tr>
<tr>
<td>14
</td>
<td>75
</td>
<td>147
</td></tr>
<tr>
<td>15
</td>
<td>100
</td>
<td>199
</td></tr></tbody></table>
</td></tr></tbody></table>

Therfore, if we wanted a maximum injury of 100 hp, we should input a value of **14** (15 - 1) in the scheme editor.