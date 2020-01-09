--returns the number of inventory slots containing at least one of a given item

function getInvStacks(item)
  local stacks = 0
  local inv = openInventory()
  local map = inv.mapping.inventory
  for i,j in pairs(map.hotbar) do
    sitem = inv.getSlot(j)
    if sitem and sitem.id == item then
      stacks = stacks + 1
    end
  end
  for i,j in pairs(map.main) do
    sitem = inv.getSlot(j)
    if sitem and sitem.id == item then
      stacks = stacks + 1
    end
  end
  inv.close()
return stacks end

return getInvStacks
