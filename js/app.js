/**
 * 行政法基本概念 102 頁互動簡報 - 核心引擎與控制邏輯
 */

document.addEventListener('DOMContentLoaded', () => {
    let currentSlideIndex = 0;
    const slides = window.slidesData || [];
    const totalSlides = slides.length;

    // DOM Elements
    const slideStage = document.getElementById('slide-stage');
    const currentSlideNumEl = document.getElementById('current-slide-num');
    const totalSlideNumEl = document.getElementById('total-slide-num');
    const progressBar = document.getElementById('progress-bar');
    const headerTitle = document.getElementById('header-title');
    const moduleBadge = document.getElementById('module-badge');

    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnToc = document.getElementById('btn-toc');
    const btnNotes = document.getElementById('btn-notes');
    const btnHelp = document.getElementById('btn-help');
    const btnFullscreen = document.getElementById('btn-fullscreen');

    const animationSelect = document.getElementById('animation-select');
    const jumpInput = document.getElementById('jump-input');
    const btnJump = document.getElementById('btn-jump');

    const notesDrawer = document.getElementById('notes-drawer');
    const closeNotes = document.getElementById('close-notes');
    const notesContent = document.getElementById('notes-content');

    const tocDrawer = document.getElementById('toc-drawer');
    const closeToc = document.getElementById('close-toc');
    const tocList = document.getElementById('toc-list');
    const tocSearch = document.getElementById('toc-search');

    const helpModal = document.getElementById('help-modal');
    const closeHelp = document.getElementById('close-help');

    // Initialize UI
    totalSlideNumEl.textContent = totalSlides;
    renderTOC();
    renderSlide(currentSlideIndex);

    // Navigation handlers
    function goToSlide(index) {
        if (index < 0 || index >= totalSlides) return;
        currentSlideIndex = index;
        renderSlide(currentSlideIndex);
        updateProgress();
        updateTOCActiveState();
    }

    btnNext.addEventListener('click', () => goToSlide(currentSlideIndex + 1));
    btnPrev.addEventListener('click', () => goToSlide(currentSlideIndex - 1));

    btnJump.addEventListener('click', () => {
        const val = parseInt(jumpInput.value, 10);
        if (val >= 1 && val <= totalSlides) {
            goToSlide(val - 1);
            jumpInput.value = '';
        }
    });

    jumpInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            btnJump.click();
        }
    });

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        switch (e.key) {
            case 'ArrowRight':
            case 'Space':
            case 'PageDown':
                e.preventDefault();
                goToSlide(currentSlideIndex + 1);
                break;
            case 'ArrowLeft':
            case 'PageUp':
                e.preventDefault();
                goToSlide(currentSlideIndex - 1);
                break;
            case 'Home':
                e.preventDefault();
                goToSlide(0);
                break;
            case 'End':
                e.preventDefault();
                goToSlide(totalSlides - 1);
                break;
            case 'm':
            case 'M':
                toggleDrawer(tocDrawer);
                break;
            case 'n':
            case 'N':
                toggleDrawer(notesDrawer);
                break;
            case 'f':
            case 'F':
                toggleFullscreen();
                break;
            case '?':
                toggleModal(helpModal);
                break;
        }
    });

    // Drawers and Modals Toggle
    function toggleDrawer(drawer) {
        drawer.classList.toggle('active');
    }
    function toggleModal(modal) {
        modal.classList.toggle('active');
    }

    btnToc.addEventListener('click', () => toggleDrawer(tocDrawer));
    closeToc.addEventListener('click', () => tocDrawer.classList.remove('active'));

    btnNotes.addEventListener('click', () => toggleDrawer(notesDrawer));
    closeNotes.addEventListener('click', () => notesDrawer.classList.remove('active'));

    btnHelp.addEventListener('click', () => toggleModal(helpModal));
    closeHelp.addEventListener('click', () => helpModal.classList.remove('active'));

    btnFullscreen.addEventListener('click', toggleFullscreen);

    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => console.log(err));
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }

    // TOC Generation & Search
    function renderTOC() {
        tocList.innerHTML = '';
        slides.forEach((slide, idx) => {
            const item = document.createElement('div');
            item.className = `toc-item ${idx === currentSlideIndex ? 'active' : ''}`;
            item.setAttribute('data-index', idx);
            item.innerHTML = `
                <span class="toc-num">Slide ${slide.id}</span>
                <span class="toc-title">${slide.title}</span>
            `;
            item.addEventListener('click', () => {
                goToSlide(idx);
                tocDrawer.classList.remove('active');
            });
            tocList.appendChild(item);
        });
    }

    tocSearch.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const items = tocList.querySelectorAll('.toc-item');
        items.forEach((item) => {
            const text = item.textContent.toLowerCase();
            if (text.includes(query)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });

    function updateTOCActiveState() {
        const items = tocList.querySelectorAll('.toc-item');
        items.forEach((item, idx) => {
            if (idx === currentSlideIndex) {
                item.classList.add('active');
                item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            } else {
                item.classList.remove('active');
            }
        });
    }

    function updateProgress() {
        currentSlideNumEl.textContent = currentSlideIndex + 1;
        const percentage = ((currentSlideIndex + 1) / totalSlides) * 100;
        progressBar.style.width = `${percentage}%`;

        btnPrev.disabled = currentSlideIndex === 0;
        btnNext.disabled = currentSlideIndex === totalSlides - 1;
    }

    // Slide Rendering Engine
    function renderSlide(index) {
        const slide = slides[index];
        if (!slide) return;

        // Apply selected or random animation class
        let animationType = animationSelect.value;
        if (animationType === 'random') {
            const availableAnims = ['slide-fade', 'zoom', 'flip', 'bounce'];
            animationType = availableAnims[Math.floor(Math.random() * availableAnims.length)];
        }
        slideStage.className = `slide-stage animation-${animationType}`;

        // Header updating
        moduleBadge.textContent = slide.module || 'Module';
        headerTitle.textContent = slide.title || '行政法基本概念';

        // Update Notes Drawer Content
        notesContent.innerHTML = slide.notes ? `
            <p><strong>【本頁的核心教導與法理延伸】</strong></p>
            <p>${slide.notes}</p>
        ` : '<p>本頁無特別補充說明。</p>';

        // Render Slide by Type
        switch (slide.type) {
            case 'cover':
                renderCoverSlide(slide);
                break;
            case 'concept':
                renderConceptSlide(slide);
                break;
            case 'comparison':
                renderComparisonSlide(slide);
                break;
            case 'multiple_choice':
                renderMultipleChoiceSlide(slide);
                break;
            case 'matching':
                renderMatchingSlide(slide);
                break;
            case 'short_answer':
                renderShortAnswerSlide(slide);
                break;
            case 'summary':
                renderSummarySlide(slide);
                break;
            default:
                renderConceptSlide(slide);
        }
    }

    // 1. Cover Slide
    function renderCoverSlide(slide) {
        slideStage.innerHTML = `
            <div class="cover-slide-content">
                <div class="cover-badge">${slide.category || '108課綱公民與社會專題'}</div>
                <h1 class="cover-title">${slide.title}</h1>
                <p class="cover-subtitle">${slide.subtitle || ''}</p>
                <div class="cover-meta">
                    <span>Target: 高中學生</span>
                    <span>Total: 102 頁素養精裝版</span>
                    <span>Topic: 行政法基礎、依法行政與權利救濟</span>
                </div>
            </div>
        `;
    }

    // 2. Concept Slide
    function renderConceptSlide(slide) {
        let contentHtml = '';
        
        if (slide.bullets) {
            contentHtml += `
                <ul class="bullet-list">
                    ${slide.bullets.map(b => `<li class="animate-item">${b}</li>`).join('')}
                </ul>
            `;
        }

        if (slide.cards) {
            contentHtml += `
                <div class="card-grid">
                    ${slide.cards.map(c => `
                        <div class="info-card animate-item">
                            <h4>${c.title}</h4>
                            <p>${c.content}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        if (slide.highlight) {
            contentHtml += `
                <div class="highlight-box animate-item">
                    💡 <strong>重點提示：</strong> ${slide.highlight}
                </div>
            `;
        }

        if (slide.caseStudy) {
            contentHtml += `
                <div class="case-box animate-item">
                    <h4>🔍 生活情境案例：${slide.caseStudy.title}</h4>
                    <p>${slide.caseStudy.content}</p>
                </div>
            `;
        }

        if (slide.quote) {
            contentHtml += `
                <div class="quote-box animate-item">
                    <h4>⚖ 司法院大法官解釋 / 憲判字典範：${slide.quote.title}</h4>
                    <p>${slide.quote.content}</p>
                </div>
            `;
        }

        if (slide.video) {
            contentHtml += `
                <div class="video-box animate-item">
                    <h4>🎥 影音法律講堂：${slide.video.title}</h4>
                    <div class="video-responsive">
                        <iframe src="https://www.youtube.com/embed/${slide.video.youtubeId}?rel=0" 
                                title="${slide.video.title}" 
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                allowfullscreen>
                        </iframe>
                    </div>
                </div>
            `;
        }

        slideStage.innerHTML = `
            <div class="slide-header-box">
                <span class="slide-category-tag">${slide.category || '觀念聚焦'}</span>
                <h2 class="slide-title">${slide.title}</h2>
                ${slide.subtitle ? `<p class="slide-subtitle">${slide.subtitle}</p>` : ''}
            </div>
            <div class="slide-content-body">
                ${contentHtml}
            </div>
        `;
    }

    // 3. Comparison Slide
    function renderComparisonSlide(slide) {
        slideStage.innerHTML = `
            <div class="slide-header-box">
                <span class="slide-category-tag">${slide.category || '概念對比剖析'}</span>
                <h2 class="slide-title">${slide.title}</h2>
                ${slide.subtitle ? `<p class="slide-subtitle">${slide.subtitle}</p>` : ''}
            </div>
            <div class="slide-content-body">
                <div class="card-grid" style="grid-template-columns: repeat(2, 1fr);">
                    <div class="info-card animate-item" style="border-top: 4px solid var(--primary);">
                        <h4>${slide.col1.title}</h4>
                        <p>${slide.col1.content}</p>
                        ${slide.col1.list ? `<ul class="bullet-list" style="margin-top:12px;">${slide.col1.list.map(i => `<li>${i}</li>`).join('')}</ul>` : ''}
                    </div>
                    <div class="info-card animate-item" style="border-top: 4px solid var(--secondary);">
                        <h4>${slide.col2.title}</h4>
                        <p>${slide.col2.content}</p>
                        ${slide.col2.list ? `<ul class="bullet-list" style="margin-top:12px;">${slide.col2.list.map(i => `<li>${i}</li>`).join('')}</ul>` : ''}
                    </div>
                </div>
                ${slide.summary ? `
                    <div class="highlight-box animate-item">
                        ⚖ <strong>差異結論：</strong> ${slide.summary}
                    </div>
                ` : ''}
            </div>
        `;
    }

    // 4. Multiple Choice Quiz Slide
    function renderMultipleChoiceSlide(slide) {
        const letters = ['A', 'B', 'C', 'D'];
        slideStage.innerHTML = `
            <div class="slide-header-box">
                <span class="slide-category-tag" style="color: var(--accent-amber);">【素養選擇題】</span>
                <h2 class="slide-title">${slide.title}</h2>
            </div>
            <div class="slide-content-body quiz-container">
                <div class="quiz-scenario animate-item">
                    📖 <strong>情境題幹：</strong> ${slide.scenario}
                </div>
                <div class="quiz-options">
                    ${slide.options.map((opt, idx) => `
                        <div class="quiz-option-card animate-item" data-index="${idx}">
                            <span class="opt-letter">${letters[idx]}</span>
                            <span>${opt}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="quiz-explanation" id="quiz-exp">
                    <h5>解析說明與法理參考：</h5>
                    <p id="quiz-exp-text">${slide.explanation}</p>
                </div>
            </div>
        `;

        // Attach Multiple Choice event listeners
        const optionCards = slideStage.querySelectorAll('.quiz-option-card');
        const expBox = slideStage.querySelector('#quiz-exp');

        optionCards.forEach(card => {
            card.addEventListener('click', () => {
                const selectedIdx = parseInt(card.getAttribute('data-index'), 10);
                
                // Clear state
                optionCards.forEach(c => c.classList.remove('selected', 'correct', 'wrong'));
                
                if (selectedIdx === slide.answerIndex) {
                    card.classList.add('correct');
                } else {
                    card.classList.add('wrong');
                    // Show the correct one as well
                    optionCards[slide.answerIndex].classList.add('correct');
                }

                expBox.classList.add('active');
            });
        });
    }

    // 5. Matching Quiz Slide
    function renderMatchingSlide(slide) {
        slideStage.innerHTML = `
            <div class="slide-header-box">
                <span class="slide-category-tag" style="color: var(--secondary);">【素養配合題】</span>
                <h2 class="slide-title">${slide.title}</h2>
                <p class="slide-subtitle">${slide.instruction || '請分別點選左欄項目與右欄相對應的情境/定義進行正確連線配對：'}</p>
            </div>
            <div class="slide-content-body matching-container">
                <div class="matching-grid">
                    <div class="matching-column" id="left-col">
                        ${slide.pairs.map((p, idx) => `
                            <div class="matching-card animate-item" data-left="${idx}" data-id="${p.id}">
                                <strong>${idx + 1}. ${p.term}</strong>
                            </div>
                        `).join('')}
                    </div>
                    <div class="matching-column" id="right-col">
                        ${shuffleArray([...slide.pairs]).map((p, idx) => `
                            <div class="matching-card animate-item" data-right="${idx}" data-match-id="${p.id}">
                                <span>${p.desc}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div class="matching-actions">
                    <button class="action-btn" id="btn-check-match">驗證配對答案</button>
                    <button class="reset-btn" id="btn-reset-match">重置連線</button>
                    <span id="matching-feedback" style="font-weight:700; font-size:1rem; margin-left:12px;"></span>
                </div>
            </div>
        `;

        let selectedLeft = null;
        let selectedRight = null;
        const userPairs = new Map(); // leftElement -> rightElement

        const leftCards = slideStage.querySelectorAll('#left-col .matching-card');
        const rightCards = slideStage.querySelectorAll('#right-col .matching-card');
        const feedback = slideStage.querySelector('#matching-feedback');

        leftCards.forEach(card => {
            card.addEventListener('click', () => {
                if (card.classList.contains('paired')) return;
                leftCards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedLeft = card;
                tryPair();
            });
        });

        rightCards.forEach(card => {
            card.addEventListener('click', () => {
                if (card.classList.contains('paired')) return;
                rightCards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedRight = card;
                tryPair();
            });
        });

        function tryPair() {
            if (selectedLeft && selectedRight) {
                selectedLeft.classList.remove('selected');
                selectedRight.classList.remove('selected');
                
                selectedLeft.classList.add('paired');
                selectedRight.classList.add('paired');

                userPairs.set(selectedLeft, selectedRight);

                selectedLeft = null;
                selectedRight = null;
            }
        }

        slideStage.querySelector('#btn-reset-match').addEventListener('click', () => {
            userPairs.clear();
            leftCards.forEach(c => c.classList.remove('paired', 'selected', 'correct', 'wrong'));
            rightCards.forEach(c => c.classList.remove('paired', 'selected', 'correct', 'wrong'));
            feedback.textContent = '';
        });

        slideStage.querySelector('#btn-check-match').addEventListener('click', () => {
            if (userPairs.size < slide.pairs.length) {
                feedback.style.color = 'var(--accent-amber)';
                feedback.textContent = '⚠️ 請完成所有項目的連線配對後再進行驗證！';
                return;
            }

            let correctCount = 0;
            userPairs.forEach((rightEl, leftEl) => {
                const targetId = leftEl.getAttribute('data-id');
                const matchedId = rightEl.getAttribute('data-match-id');
                if (targetId === matchedId) {
                    correctCount++;
                }
            });

            if (correctCount === slide.pairs.length) {
                feedback.style.color = 'var(--accent-green)';
                feedback.textContent = `🎉 太棒了！全部 ${correctCount} 組配對完全正確！`;
            } else {
                feedback.style.color = 'var(--accent-red)';
                feedback.textContent = `❌ 配對完成，答對 ${correctCount} / ${slide.pairs.length} 組。按下重置再試一次！`;
            }
        });
    }

    // Utility shuffle array function
    function shuffleArray(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    // 6. Short Answer Slide
    function renderShortAnswerSlide(slide) {
        slideStage.innerHTML = `
            <div class="slide-header-box">
                <span class="slide-category-tag" style="color: var(--accent-green);">【素養簡答思考題】</span>
                <h2 class="slide-title">${slide.title}</h2>
            </div>
            <div class="slide-content-body short-answer-container">
                <div class="quiz-scenario animate-item">
                    💬 <strong>情境問題思考：</strong> ${slide.prompt}
                </div>
                <div class="animate-item">
                    <textarea class="short-answer-input" placeholder="請在此輸入您的思考與作答內容（可作為課堂討論或個人思考整理）..."></textarea>
                </div>
                <div class="matching-actions animate-item">
                    <button class="action-btn" id="btn-toggle-model-ans">顯示參考解答與採分關鍵點</button>
                </div>
                <div class="model-answer-card" id="model-ans-box">
                    <h5>⚖ 官方標竿參考解答：</h5>
                    <p>${slide.modelAnswer}</p>
                    <div class="scoring-points">
                        <h6>🎯 作答採分關鍵字 (Key Concepts)：</h6>
                        <ul class="bullet-list" style="margin-top:6px;">
                            ${slide.keyPoints.map(k => `<li>${k}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;

        const btnToggle = slideStage.querySelector('#btn-toggle-model-ans');
        const modelBox = slideStage.querySelector('#model-ans-box');

        btnToggle.addEventListener('click', () => {
            modelBox.classList.toggle('active');
            if (modelBox.classList.contains('active')) {
                btnToggle.textContent = '隱藏參考解答';
            } else {
                btnToggle.textContent = '顯示參考解答與採分關鍵點';
            }
        });
    }

    // 7. Summary Slide
    function renderSummarySlide(slide) {
        slideStage.innerHTML = `
            <div class="slide-header-box">
                <span class="slide-category-tag">${slide.category || '本章觀念心智圖與小結'}</span>
                <h2 class="slide-title">${slide.title}</h2>
            </div>
            <div class="slide-content-body">
                <div class="card-grid">
                    ${slide.summaryCards.map(c => `
                        <div class="info-card animate-item" style="background: rgba(99, 102, 241, 0.08); border-color: rgba(99, 102, 241, 0.3);">
                            <h4 style="color:#fff;">${c.title}</h4>
                            <p>${c.content}</p>
                        </div>
                    `).join('')}
                </div>
                ${slide.conclusion ? `
                    <div class="highlight-box animate-item" style="margin-top: 10px;">
                        📌 <strong>核心精神結語：</strong> ${slide.conclusion}
                    </div>
                ` : ''}
            </div>
        `;
    }
});
