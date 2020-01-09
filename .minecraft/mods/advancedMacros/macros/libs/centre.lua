--attempts to centre the player on the current block

function centre()
  local x,y,z=getPlayerBlockPos()
  sneak(-1)
  forward(-1)
  for i=0,20 do
    lookAt(x+0.5,y+1.5,z+0.5)
    sleep(20)
  end
  forward(0)
  sneak(0)
return end

return centre
