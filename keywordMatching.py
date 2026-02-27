def calculate_match_score(query, title):
    """
    Calculate the percentage of quey words found in the job title.
    """
    if not query or not title:
        return 0.0
    
    query_words = query.lower().split()
    title_lower =title.lower()
    
    match_count = sum(1 for word in query_words if word in title_lower)
    
    return match_count / len(query_words)
    