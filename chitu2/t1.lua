
-- split

local function xsplit(inputstr, sep)
        if sep == nil then
                sep = "%s"
        end
        local t={} ; local i=1
        for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
                t[i] = str
                i = i + 1
        end
        return t
end

--

redis.call('HSET', KEYS[1], KEYS[2], ARGV[1] )
redis.call('HSET', KEYS[1], 'timestamp', ARGV[2] )

-- 

local k = KEYS[1]..'_count'

redis.call("INCR",k)

return xsplit(ARGV[1],'%s')[6]