from random import randint
from prop import genProp, getArgs, hasContr, Rule

prop_len = 3
depth_param = 2 # 9: d ~ 7, w ~ 4

root_prop = genProp(randint(3,prop_len))
prop_stack = [root_prop]
hypothesis = []
first_rule = None
while len(prop_stack) > 0:
    top = prop_stack.pop()
    new_rule = None
    if randint(0,depth_param) == 0 and top != 'F' and not hasContr(hypothesis,top):
        new_rule = Rule.Hyp_Intr
        if first_rule == None:
            first_rule = new_rule
        hypothesis.append(top)
    else:   # Choose one applyable rule and create the child prop(s)
        if top in hypothesis:
            available_rules = [Rule.Hyp_Intr]
        elif top == 'F':
            available_rules = [Rule.NOT_Elim]
        elif top[0] == '^':
            available_rules = [Rule.F_Elim,Rule.AND_Elim_L,Rule.AND_Elim_R,Rule.AND_Intr]
        elif top[0] == '~':
            available_rules = [Rule.F_Elim,Rule.AND_Elim_L,Rule.AND_Elim_R,Rule.NOT_Intr]
        else:
            available_rules = [Rule.F_Elim,Rule.AND_Elim_L,Rule.AND_Elim_R]
        
        new_rule = available_rules[randint(0,len(available_rules)-1)]
        if first_rule == None:
            first_rule = new_rule
        
        if new_rule == Rule.F_Elim:
            prop_stack.append('F')
        elif new_rule == Rule.NOT_Intr:
            prop_stack.append('F')
            hypothesis.append(top[1:]) #
        elif new_rule == Rule.NOT_Elim:
            new_prop = genProp(randint(3,prop_len))
            prop_stack.append(new_prop)
            prop_stack.append('~'+new_prop)
        elif new_rule == Rule.AND_Elim_L:
            new_prop = genProp(randint(3,prop_len))
            prop_stack.append('^'+new_prop+top)
        elif new_rule == Rule.AND_Elim_R:
            new_prop = genProp(randint(3,prop_len))
            prop_stack.append('^'+top+new_prop)
        elif new_rule == Rule.AND_Intr:
            prop_left, prop_right = getArgs(top)
            prop_stack.append(prop_left)
            prop_stack.append(prop_right)
        elif new_rule != Rule.Hyp_Intr:
            print('Cant apply rule to prop',top,new_rule)
    print(top,new_rule.name)

print(root_prop,hypothesis,first_rule)

