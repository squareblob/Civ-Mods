--eats food if the player is hungry, starting with the worst

function autoEat(pslot,timeout)
  pslot = pslot or 9
  timeout = timeout or 10
  package.loaded.pick = nil
  pick = require("pick")
  foods = {"minecraft:beetroot",
           "minecraft:cookie",
           "minecraft:melon_slice",
           --"minecraft:apple",
           "minecraft:chorus_fruit",
           "minecraft:carrot",
           "minecraft:baked_potato",
           "minecraft:bread",
           "minecraft:pumpkin_pie",
           "minecraft:cooked_chicken",
           "minecraft:cooked_mutton",
           "minecraft:cooked_porkchop",
           "minecraft:cooked_beef"}
  t = 0
  hf = false
  if getPlayer().hunger < 20 then
    --log("having some food...")
  else
    --log("not hungry, not eating")
    return
  end
  while getPlayer().hunger < 20 and t < timeout do
    for n,f in pairs(foods) do
      i = pick(f,-1,pslot)
      if i then 
        hf = true
        break
      end
    end
    if not hf then
      --log("cannot find food")
      break
    else
      use(2500)
      sleep(2500)
      t = t + 1
    end
  end
  if getPlayer().hunger == 20 then
    --log("finished eating")
    return true
  else
    --log("eating timed out")
    return false
  end
end

return autoEat

