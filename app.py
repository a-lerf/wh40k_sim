# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:30:17 2021

@author: kanbei

v 0.1.1 
"""

import streamlit as st
import numpy as np
import pandas as pd

att_type = ['Ranged','Melee']
a_reroll = ['None','Ones','All']
d_reroll = ['None','Ones','All']

#create streamlit elements on main page
st.title('Warhammer 40k 9th ed calculator')
st.write('v 0.1.1')
att_type_select = st.sidebar.selectbox('Select attack type', (att_type))

if att_type_select == att_type[0]:
    skill_label = 'Ballistic skill'
else: 
    skill_label = 'Weapon skill'
    
num_attackers = st.sidebar.number_input('Number of attacks', min_value = 1, step = 1)
num_defenders = st.sidebar.number_input('Number of defenders', min_value = 1, step = 1)

st.header('Attacker')

a_col1, a_col2, a_col3, a_col4 = st.beta_columns(4) 

with a_col1:
    a_skill = st.number_input(skill_label, min_value = 1, max_value = 6, step = 1, value = 3)
    a_hit_reroll = st.selectbox('Hit reroll', (a_reroll))
    
with a_col2:
    a_strength = st.number_input('Strength', min_value = 0, step = 1, value = 3)
    
with a_col3:
    a_armor_p = st.number_input('Armor Piercing', min_value = -10, step = 1, value = 0)
    a_wound_reroll = st.selectbox('Wound reroll', (a_reroll))
    
with a_col4:
    a_damage = st.number_input('Damage', min_value = 1, max_value = 10, step = 1)
    #a_plasma = st.checkbox('Plasma')

# with st.beta_expander('Additional settings'):
#     st.write('wip')
    
    
st.header('Defender')

d_col1, d_col2, d_col3, d_col4 = st.beta_columns(4)

with d_col1:
    d_tough = st.number_input('Toughness', min_value = 0, step = 1, value = 1)
    d_wounds = st.number_input('Wounds', min_value = 1, step = 1)
    
with d_col2:
    d_save = st.number_input('Save Roll', min_value = 2, step = 1)
    
with d_col3:
    d_save_mod = st.number_input('Save modifier', min_value = -10, step = 1, value = 0)
    d_save_reroll = st.selectbox('Save reroll', (d_reroll))
    
with d_col4:
    d_invul = st.number_input('Invulnerable', min_value = 2, max_value = 7, step = 1, value = 7)
    d_invul_reroll = st.selectbox('Reroll', (d_reroll))
    
# with st.beta_expander('Additional settings'):
#     st.write('wip')
    
def roll_hits(num_a):
    hit_list = np.random.randint(1,7,(num_a,1))
    count = 0
    for i in hit_list:
        if a_hit_reroll == a_reroll[1]:
            if i[0] >= a_skill:
                count+=1
            elif i[0] == 1:
                if np.random.randint(1,7) >= a_skill:
                    count+=1
            
        elif a_hit_reroll == a_reroll[2]:
            if i[0] >= a_skill:
                count+=1
            else:
                if np.random.randint(1,7) >= a_skill:
                    count+=1
            
        else:
            if i[0] >= a_skill:
                count+=1
                
    return count

def roll_wounds(num_h):
    if a_strength >= 2*d_tough:
        req = 2
    elif a_strength > d_tough:
        req = 3
    elif a_strength == d_tough:
        req = 4
    elif a_strength <= d_tough/2:
        req = 6   
    elif a_strength < d_tough:
        req = 5
    else:
        req = 6
        
    att_list = np.random.randint(1,7,(num_h,1))
    count = 0
    for i in att_list:
        if a_wound_reroll == a_reroll[1]:
            if i[0] >= req:
                count+=1
            elif i[0] == 1:
                if np.random.randint(1,7) >= req:
                    count+=1
            
        elif a_wound_reroll == a_reroll[2]:
            if i[0] >= req:
                count+=1
            else:
                if np.random.randint(1,7) >= req:
                    count+=1
            
        else:
            if i[0] >= req:
                count+=1
    return count

def roll_saves(num_w):
    req = d_save-a_armor_p-d_save_mod
        
    wound_list = np.random.randint(1,7,(num_w,1))
    count = 0
    for i in wound_list:
        if d_save_reroll == d_reroll[1]:
            if i[0] >= req:
                count+=1
            elif i[0] == 1:
                if np.random.randint(1,7) >= req:
                    count+=1
            
        elif d_save_reroll == d_reroll[2]:
            if i[0] >= req:
                count+=1
            else:
                if np.random.randint(1,7) >= req:
                    count+=1
            
        else:
            if i[0] >= req:
                count+=1
        
    return count

def roll_invul(num_rw):
            
    wound_list = np.random.randint(1,7,(num_rw,1))
    count = 0
    for i in wound_list:
        if d_invul_reroll == d_reroll[1]:
            if i[0] >= d_invul:
                count+=1
            elif i[0] == 1:
                if np.random.randint(1,7) >= d_invul:
                    count+=1
            
        elif d_invul_reroll == d_reroll[2]:
            if i[0] >= d_invul:
                count+=1
            else:
                if np.random.randint(1,7) >= d_invul:
                    count+=1
            
        else:
            if i[0] >= d_invul:
                count+=1
        
    return count

def sim_attack(num_sim):
    '''
    create dataframe from all battle rounds
    '''
    hit_count_list = []
    wound_count_list = []
    save_count_list = []
    invul_count_list = []
    final_save_list = []
    realized_wound_list = []
    realized_wound_final_list = []
    damage_list = []
    for i in range(num_sim):
        hit_count = roll_hits(num_attackers)
        hit_count_list.append(hit_count)
        wound_count = roll_wounds(hit_count)
        wound_count_list.append(wound_count)
        save_count = roll_saves(wound_count)
        save_count_list.append(save_count)
        realized_wounds = wound_count-save_count
        realized_wound_list.append(realized_wounds)
        invul_count = roll_invul(realized_wounds)
        invul_count_list.append(invul_count)
        final_save_count = save_count + invul_count
        final_save_list.append(final_save_count)
        realized_wounds_final = wound_count-final_save_count
        realized_wound_final_list.append(realized_wounds_final)
        damage = realized_wounds_final*a_damage
        damage_list.append(damage)
        
    attr_dict = {'hits':hit_count_list,
                 'wounds':wound_count_list, 
                 'saves': save_count_list,
                 'invul': invul_count_list,
                 'final_wounds': realized_wound_final_list,
                 'damage': damage_list}
    
    df = pd.DataFrame(attr_dict)
        
    return df

num_sim = st.sidebar.number_input('Number of Simulations', min_value = 1, max_value = 100000,step = 1, value = 10000)

st.header('Results')
if st.sidebar.button('Simulate'):
    if att_type_select == att_type[0]:
    
        df = sim_attack(num_sim)   
        
        r_col1, r_col2, r_col3 = st.beta_columns(3)
        r_col4, r_col5, r_col6 = st.beta_columns(3)
    
        with r_col1:
            st.text('Hit rolls')
            st.pyplot(df['hits'].plot.hist(range = [0,num_attackers]).get_figure(), clear_figure= True)
            st.text('Average hits: ' + str(df['hits'].mean()))
            
        with r_col2:
            st.text('Wound rolls')
            st.pyplot(df['wounds'].plot.hist(range = [0,num_attackers]).get_figure(), clear_figure= True)
            st.text('Average wound rolls: ' + str(df['wounds'].mean()))
    
        with r_col3:
            st.text('Save rolls')
            st.pyplot(df['saves'].plot.hist(range = [0,num_attackers]).get_figure(), clear_figure= True)
            st.text('Average saves: ' + str(df['saves'].mean()))
            
        with r_col4:
            st.text('Invulnerable save rolls')
            st.pyplot(df['invul'].plot.hist(range = [0,num_attackers]).get_figure(), clear_figure= True)
            st.text('Average invul: ' + str(df['invul'].mean()))
    
        with r_col5:
            st.text('Final wounds')
            st.pyplot(df['final_wounds'].plot.hist(range = [0,num_attackers]).get_figure(), clear_figure= True)
            st.text('Hits on target: ' + str(df['final_wounds'].mean()))
            
        with r_col6:
            st.text('Damage')
            st.pyplot(df['damage'].plot.hist(range = [0,num_attackers*a_damage]).get_figure(), clear_figure= True)
            st.text('Average damage: ' + str(df['damage'].mean()))
            
        count_wounds = num_defenders*d_wounds  
        perc_wounds = df['damage'].mean()/count_wounds*100
        damage_per_attack = df['damage'].mean()/num_attackers
        st.text('Attackers deal approximately ' + str(perc_wounds)[:4] +'% of the total wounds as damage from ' + str(num_attackers) + ' attacks.')
        st.text(str(num_defenders) + ' defender(s) take(s) ' + str(damage_per_attack)[:4] + ' damage per attack on average.')
        
    elif att_type_select == att_type[1]: 
        st.text('Melee not implemented yet, check back soon!')
        
else:
    st.text('Please choose all parameters and hit Simulate in the sidebar!')
    