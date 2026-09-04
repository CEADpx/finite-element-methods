local problem_number = 0

function Header(header)
  if not header.classes:includes("problem") then
    return nil
  end

  local marks = header.attributes["marks"]
  if marks == nil or marks == "" then
    error("Every problem heading must provide a marks attribute.")
  end

  problem_number = problem_number + 1
  local unit = marks == "1" and "mark" or "marks"
  local original_title = header.content

  header.content = pandoc.Inlines({
    pandoc.Str("Problem"),
    pandoc.Space(),
    pandoc.Str(tostring(problem_number)),
    pandoc.Space(),
    pandoc.Str("(" .. marks .. " " .. unit .. "):"),
    pandoc.Space(),
  })

  for _, inline in ipairs(original_title) do
    header.content:insert(inline)
  end

  header.attributes["marks"] = nil
  return header
end
