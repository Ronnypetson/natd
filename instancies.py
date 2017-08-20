from __future__ import print_function
from random import randint
from prop import genProp, getArgs, hasContr, isNeg, Rule

# Hyperparameters
# Small trees: prop_len = 4, depth_param = 1, gen_len = prop_len - 2
prop_len = 5
gen_len = prop_len-2
depth_param = 2

#
root_prop = genProp(randint(1,prop_len))
prop_stack = [root_prop]
hypothesis = []
virt_hyp = ['T']
first_rule = None
while len(prop_stack) > 0:
    top = prop_stack.pop()
    virt_hyp.pop()
    new_rule = None
    if randint(0,depth_param) == 0 and top != 'F' and not hasContr(hypothesis,top) and not top == root_prop:    # Check if top can be a hypothesis
        new_rule = Rule.Hyp_Intr
        if first_rule == None:
            first_rule = new_rule
        if not top in hypothesis:
            hypothesis.append(top)
    else:   # Choose one applyable rule and create the child prop(s)
        if top in hypothesis or (top != 'T' and top in virt_hyp):
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
        if new_rule == Rule.AND_Intr or new_rule == Rule.AND_Elim_L or new_rule == Rule.AND_Elim_R:   # Assignes low probability for AND_Intr
            new_rule = available_rules[randint(0,len(available_rules)-1)]
        
        if first_rule == None:
            first_rule = new_rule
        
        if new_rule == Rule.F_Elim:
            prop_stack.append('F')
            virt_hyp.append('T')
        elif new_rule == Rule.NOT_Intr:
            prop_stack.append('F')
            virt_hyp.append(top[1:])
        elif new_rule == Rule.NOT_Elim:
            # Check for available hypothesis first
            exit = False
            for v in virt_hyp:
                for h in hypothesis:
                    exit = True
                    if isNeg(v,h):
                        prop_stack.append(h)
                        prop_stack.append(v)                        
                    elif isNeg(h,v):
                        prop_stack.append(h)
                        prop_stack.append(v)
                    else:
                        exit = False
                    if exit:
                        break
                if exit:
                    break
            if not exit:
                use_virt = False
                for v in virt_hyp:
                    if v != 'T':
                        use_virt = True
                if len(virt_hyp) > 0 and use_virt:
                    virt = 'T'
                    while virt == 'T':
                        virt = virt_hyp[randint(0,len(virt_hyp)-1)]
                    if virt[0] == '~':
                        prop_stack.append(virt[1:])
                        prop_stack.append(virt)
                    else:
                        prop_stack.append(virt)
                        prop_stack.append('~'+virt)
                elif len(hypothesis) > 0:
                    hyp = hypothesis[randint(0,len(hypothesis)-1)]
                    if hyp[0] == '~':
                        prop_stack.append(hyp[1:])
                        prop_stack.append(hyp)
                    else:
                        prop_stack.append(hyp)
                        prop_stack.append('~'+hyp)
                else:
                    new_prop = genProp(randint(1,gen_len))
                    prop_stack.append(new_prop)
                    prop_stack.append('~'+new_prop)
            virt_hyp.append('T')
            virt_hyp.append('T')
        elif new_rule == Rule.AND_Elim_L:
            new_prop = genProp(randint(1,gen_len))
            prop_stack.append('^'+new_prop+top)
            virt_hyp.append('T')
        elif new_rule == Rule.AND_Elim_R:
            new_prop = genProp(randint(1,gen_len))
            prop_stack.append('^'+top+new_prop)
            virt_hyp.append('T')
        elif new_rule == Rule.AND_Intr:
            prop_left, prop_right = getArgs(top)
            prop_stack.append(prop_left)
            prop_stack.append(prop_right)
            virt_hyp.append('T')
            virt_hyp.append('T')
        elif new_rule != Rule.Hyp_Intr:
            print('Cant apply rule to prop',top,new_rule)
    print(prop_stack,hypothesis,virt_hyp,new_rule.name)
    #print(top,'         ',new_rule.name)

# Print the generated instance
print()
print(root_prop)
for h in hypothesis:
    print(h, end=' ')
print()
print(first_rule.name)

