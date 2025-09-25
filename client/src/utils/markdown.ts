/**
 * Utility function to format markdown text to HTML
 * Supports common markdown syntax like bold, italic, headers, lists, and code blocks
 */
export const formatMarkdown = (text: string): string => {
  if (!text) return ''
  
  let formatted = text
    // Bold text: **text** or __text__
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/__(.*?)__/g, '<strong>$1</strong>')
    
    // Italic text: *text* or _text_ (but not if already in bold)
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
    .replace(/(?<!_)_([^_]+)_(?!_)/g, '<em>$1</em>')
    
    // Headers: # ## ###
    .replace(/^### (.*$)/gm, '<h3 class="text-h6 font-weight-bold mb-2 mt-4 text-olive-green">$1</h3>')
    .replace(/^## (.*$)/gm, '<h2 class="text-h5 font-weight-bold mb-3 mt-4 text-azure-blue">$1</h2>')
    .replace(/^# (.*$)/gm, '<h1 class="text-h4 font-weight-bold mb-3 mt-4 text-olive-green">$1</h1>')
    
    // Code blocks: `code`
    .replace(/`([^`]+)`/g, '<code class="bg-grey-lighten-3 pa-1 rounded text-red-darken-2">$1</code>')
    
    // Lists: - item or * item (with proper nesting)
    .replace(/^(\s*)[-*] (.*)$/gm, (match, indent, content) => {
      const level = Math.floor(indent.length / 2)
      return `<li class="mb-1" style="margin-left: ${level * 20}px">${content}</li>`
    })
    
    // Numbered lists: 1. item
    .replace(/^(\s*)(\d+)\. (.*)$/gm, (match, indent, num, content) => {
      const level = Math.floor(indent.length / 2)
      return `<li class="mb-1" style="margin-left: ${level * 20}px">${content}</li>`
    })
    
    // Line breaks (preserve double line breaks as paragraphs)
    .replace(/\n\n/g, '</p><p class="mb-3">')
    .replace(/\n/g, '<br>')
  
  // Wrap content in paragraph tags if not already wrapped
  if (!formatted.includes('<p>') && !formatted.includes('<h1>') && !formatted.includes('<h2>') && !formatted.includes('<h3>')) {
    formatted = `<p class="mb-3">${formatted}</p>`
  }
  
  // Wrap lists in ul tags
  formatted = formatted.replace(/(<li[^>]*>.*?<\/li>)/gs, (match) => {
    // Check if already wrapped in ul/ol
    if (formatted.includes('<ul>') || formatted.includes('<ol>')) {
      return match
    }
    return `<ul class="ml-4 mb-3">${match}</ul>`
  })
  
  return formatted
}

/**
 * Sanitize HTML to prevent XSS attacks while preserving formatting
 */
export const sanitizeHtml = (html: string): string => {
  // Basic sanitization - remove script tags and dangerous attributes
  return html
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/on\w+="[^"]*"/g, '')
    .replace(/javascript:/gi, '')
}

/**
 * Format markdown with sanitization
 */
export const formatAndSanitizeMarkdown = (text: string): string => {
  const formatted = formatMarkdown(text)
  return sanitizeHtml(formatted)
}