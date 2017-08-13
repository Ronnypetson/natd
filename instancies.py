from random import randint
from prop import genProp, getArgs, Rule

prop_len = 10
depth_param = 12 # d ~ 7, w ~ 4

root_prop = genProp(randint(5,prop_len))
prop_stack = [root_prop]
hypothesis = []
first_rule = None
while len(prop_stack) > 0:
    top = prop_stack.pop()
    if randint(0,depth_param) == 0:
        if first_rule == None:
            first_rule = Rule.Hyp_Intr
        hypothesis.append(top)
    else:   # Choose one applyable rule and create the child prop(s)
        available_rules = [Rule.AND_Elim_L, Rule.AND_Elim_R, Rule.F_Elim]
        if top == 'F':
            available_rules.append(Rule.NOT_Elim)
        elif top[0] == '^':
            available_rules.append(Rule.AND_Intr)
        elif top[0] == '~':
            available_rules.append(Rule.NOT_Intr)
        
        new_rule = available_rules[randint(0,len(available_rules)-1)]
        if first_rule == None:
            first_rule = new_rule
        
        if new_rule == Rule.F_Elim:
            prop_stack.append('F')
        elif new_rule == Rule.NOT_Intr:
            prop_stack.append('F')
        elif new_rule == Rule.NOT_Elim:
            new_prop = genProp(randint(5,prop_len/2))
            prop_stack.append(new_prop)
            prop_stack.append('~'+new_prop)
        elif new_rule == Rule.AND_Elim_L:
            new_prop = genProp(randint(5,prop_len/2))
            prop_stack.append('^'+new_prop+top)
        elif new_rule == Rule.AND_Elim_R:
            new_prop = genProp(randint(5,prop_len/2))
            prop_stack.append('^'+new_prop+top)
        elif new_rule == Rule.AND_Intr:
            prop_left, prop_right = getArgs(top)
            prop_stack.append(prop_left)
            prop_stack.append(prop_right)
        else:
            print('Cant apply rule to prop',top,new_rule)

print(root_prop,hypothesis,first_rule)

