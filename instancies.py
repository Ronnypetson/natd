from random import randint
from prop import genProp, getArgs, Rule

prop_len = 10
depth_param = 4 # 9: d ~ 7, w ~ 4

root_prop = genProp(randint(5,prop_len))
prop_stack = [root_prop]
hypothesis = []
first_rule = None
while len(prop_stack) > 0:
    top = prop_stack.pop()
    if randint(0,depth_param) == 0:
        if first_rule == None:
            first_rule = Rule.Hyp_Intr
        if top != 'F':
            hypothesis.append(top)
    else:   # Choose one applyable rule and create the child prop(s)
        if top in hypothesis:
            available_rules = [Rule.Hyp_Intr]
        elif top == 'F':
            available_rules = [Rule.F_Elim,Rule.NOT_Elim]
        elif top[0] == '^':
            available_rules = [Rule.F_Elim,Rule.AND_Elim_L,Rule.AND_Elim_R,Rule.AND_Intr]
        elif top[0] == '~':
            available_rules = [Rule.F_Elim,Rule.AND_Elim_L,Rule.AND_Elim_R,Rule.NOT_Intr]
        
        new_rule = available_rules[randint(0,len(available_rules)-1)]
        if first_rule == None:
            first_rule = new_rule
        
        if new_rule == Rule.F_Elim:
            prop_stack.append('F')
        elif new_rule == Rule.NOT_Intr:
            prop_stack.append('F')
        elif new_rule == Rule.NOT_Elim:
            new_prop = genProp(randint(5,prop_len))
            prop_stack.append(new_prop)
            prop_stack.append('~'+new_prop)
        elif new_rule == Rule.AND_Elim_L:
            new_prop = genProp(randint(5,prop_len))
            prop_stack.append('^'+new_prop+top)
        elif new_rule == Rule.AND_Elim_R:
            new_prop = genProp(randint(5,prop_len))
            prop_stack.append('^'+top+new_prop)
        elif new_rule == Rule.AND_Intr:
            prop_left, prop_right = getArgs(top)
            prop_stack.append(prop_left)
            prop_stack.append(prop_right)
        elif new_rule != Rule.Hyp_Intr:
            print('Cant apply rule to prop',top,new_rule)

print(root_prop,hypothesis,first_rule)

