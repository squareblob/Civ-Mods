--lua implementation of macromod's pick() function
--optionally sets preffered slot and minimum durability for tools
--selects item in hotbar if present
--shift-clicks item into preferred slot if in inventory
--returns false if no item in inventory

function pick(item, slot, dmg)
  local inv = openInventory()
  local map = inv.mapping.inventory
  slot = slot or 1
  dmg = dmg or -1
  
  held = getInventory()[getHotbar()]
  if held and (held.id==item and (dmg==-1 or dmg>=item.dmg)) then
    return getHotbar()
  end
  
  for i,j in pairs(map.hotbar) do
    local hotbarItem = inv.getSlot(j)
    if hotbarItem and (hotbarItem.id==item and (dmg==-1 or dmg>=hotbarItem.dmg)) then
      setHotbar(i)
      return j
    end
  end
  
  for i,j in pairs(map.main) do
    local invItem = inv.getSlot(j)
    if invItem and (invItem.id==item and (dmg==-1 or dmg>=invItem.dmg))  then
      setHotbar(slot)
      local p = map.hotbar[slot]
      inv.quick(p)
      inv.quick(j)
      return slot
    end
    inv.close()
  end
  return false
end

return pick
